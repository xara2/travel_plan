"""ReAct Agent with task decomposition, tool use, and conversation memory."""
from __future__ import annotations
import json
import re
from .llm_client import get_llm_client
from .tool_registry import get_tool_registry

MAX_ITERATIONS = 10

SYSTEM_PROMPT = """你是一个专业的旅行规划助手，拥有以下能力：

## 可用工具

1. **search_attractions** — 语义搜索景点
   参数: query(搜索关键词), city(城市), category(类别), top_k(数量)
   用途: 当用户想找特定类型的景点时使用，如"适合亲子的海滩"、"历史文化景点"

2. **generate_plan** — 生成旅行计划
   参数: attraction_ids(景点ID的JSON数组), destination(目的地), duration(天数), preferences(偏好)
   用途: 当用户选好景点后，生成按天分配的旅行计划

3. **search_images** — 搜索景点图片
   参数: query(关键词), destination(目的地), count(数量)
   用途: 当用户想看目的地或景点的实际照片时使用

## 工作流程

收到用户请求后，按以下步骤处理：
1. 分析用户意图，确定需要调用哪些工具
2. 如果用户想搜索景点 → 调用 search_attractions
3. 如果用户选好景点想生成计划 → 调用 generate_plan
4. 如果用户想看图片 → 调用 search_images
5. 综合工具返回的结果，用自然语言回复用户

## 回复格式

- 如果需要调用工具，请用以下 JSON 格式回复，不要包含其他内容:
  {"tool": "工具名", "args": {"参数名": "参数值", ...}}
- 如果不需要调用工具，直接回复用户
- 如果用户只是聊天问候，友好回复即可

## 重要规则

- 一次只调用一个工具
- 景点ID从搜索结果中获取，不要编造
- 计划生成后要总结关键信息（天数、每天景点数、门票总费用）
- 保持回复简洁、实用、友好
- 所有回复使用中文"""


class ConversationMemory:
    """Manages conversation history with auto-summarization."""

    MAX_HISTORY = 15

    def __init__(self, conversation):
        self.conversation = conversation
        self._summary: str | None = None

    def build_messages(self, system_prompt: str = SYSTEM_PROMPT) -> list[dict]:
        messages = [{"role": "system", "content": system_prompt}]

        # Add summary if exists
        if self.conversation.context_json and self.conversation.context_json.get("summary"):
            messages.append({
                "role": "system",
                "content": f"[对话历史摘要] {self.conversation.context_json['summary']}",
            })

        # Add recent messages
        msgs = sorted(self.conversation.messages, key=lambda m: m.created_at or "")
        recent = msgs[-self.MAX_HISTORY:] if len(msgs) > self.MAX_HISTORY else msgs

        for m in recent:
            content = m.content
            if m.metadata_json and m.metadata_json.get("tool_calls"):
                content = f"[工具调用结果] {content}"
            messages.append({"role": m.role, "content": content})

        return messages

    async def maybe_summarize(self, llm):
        """Summarize early messages when history grows beyond MAX_HISTORY."""
        msgs = sorted(self.conversation.messages, key=lambda m: m.created_at or "")
        if len(msgs) <= self.MAX_HISTORY:
            return

        # Messages to summarize (everything before the last MAX_HISTORY)
        to_summarize = msgs[:-self.MAX_HISTORY]
        if not to_summarize:
            return

        lines = []
        for m in to_summarize:
            lines.append(f"[{m.role}]: {m.content[:200]}")

        summary_prompt = f"请用2-3句话总结以下旅行规划对话的关键信息（目的地、偏好、已选景点等）：\n" + "\n".join(lines)

        try:
            summary = await llm.chat(
                messages=[{"role": "user", "content": summary_prompt}],
                temperature=0.3,
                max_tokens=300,
            )
            self.conversation.context_json = self.conversation.context_json or {}
            self.conversation.context_json["summary"] = summary.strip()
            self._summary = summary.strip()
        except Exception:
            pass


class ReActAgent:
    def __init__(self):
        self.llm = get_llm_client()
        self.tool_registry = get_tool_registry()

    async def run(self, memory: ConversationMemory, user_message: str) -> str:
        """Execute the ReAct loop for a user message."""
        # Build initial messages
        messages = memory.build_messages()
        messages.append({"role": "user", "content": user_message})

        iteration = 0
        tool_calls = []

        while iteration < MAX_ITERATIONS:
            iteration += 1

            # Get LLM response
            try:
                response = await self.llm.chat(
                    messages=messages,
                    temperature=0.7,
                    max_tokens=2000,
                )
            except Exception as e:
                error_msg = str(e)
                if "InvalidApiKey" in error_msg or "No API-key" in error_msg:
                    return "抱歉，AI 服务尚未配置。请在后台设置 LLM_API_KEY 环境变量。"
                elif "timeout" in error_msg.lower():
                    return "AI 服务响应超时，请稍后再试。"
                else:
                    return f"抱歉，AI 服务暂时不可用：{error_msg[:100]}"

            # Try to parse tool call from response
            tool_call = self._parse_tool_call(response)

            if tool_call:
                tool_name = tool_call["tool"]
                tool_args = tool_call["args"]

                # Execute tool
                observation = await self.tool_registry.call(tool_name, **tool_args)
                tool_calls.append({
                    "tool": tool_name,
                    "args": tool_args,
                    "observation": observation[:500],
                })

                # Append interaction to message history
                messages.append({"role": "assistant", "content": response})
                messages.append({
                    "role": "user",
                    "content": f"[工具 {tool_name} 返回结果]\n{observation}",
                })
            else:
                # Final response — no more tool calls needed
                return response

        # Max iterations reached — synthesize final answer
        return await self._force_synthesize(messages, tool_calls)

    def _parse_tool_call(self, response: str) -> dict | None:
        """Extract tool call JSON from LLM response."""
        # Try to find JSON block
        json_match = re.search(r'\{[^{}]*"tool"\s*:\s*"[^"]+"[^{}]*\}', response, re.DOTALL)
        if json_match:
            try:
                parsed = json.loads(json_match.group(0))
                tool_name = parsed.get("tool", "")
                if tool_name in self.tool_registry.get_tool_names():
                    return parsed
            except json.JSONDecodeError:
                pass

        # Try full JSON parse
        try:
            parsed = json.loads(response.strip())
            if isinstance(parsed, dict) and "tool" in parsed:
                return parsed
        except json.JSONDecodeError:
            pass

        return None

    async def _force_synthesize(self, messages: list[dict], tool_calls: list[dict]) -> str:
        """Force a final synthesis when max iterations reached."""
        synth_prompt = (
            "请根据以上工具调用结果，为用户生成最终的旅行建议回复。"
            "综合搜索结果和建议，简洁清晰地回复。"
        )
        messages.append({"role": "user", "content": synth_prompt})
        try:
            return await self.llm.chat(messages=messages, temperature=0.7, max_tokens=1500)
        except Exception:
            return "抱歉，处理您的请求时遇到了一些问题。请稍后再试。"
