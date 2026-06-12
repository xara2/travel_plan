"""Tool registry — singleton for registering and dispatching agent tools."""
from __future__ import annotations


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, dict] = {}

    def register(self, name: str, description: str, handler, parameters: dict | None = None):
        self._tools[name] = {
            "name": name,
            "description": description,
            "handler": handler,
            "parameters": parameters or {},
        }

    def list_tools(self) -> list[dict]:
        return [
            {"name": t["name"], "description": t["description"], "parameters": t["parameters"]}
            for t in self._tools.values()
        ]

    async def call(self, name: str, **kwargs) -> str:
        tool = self._tools.get(name)
        if not tool:
            return f"错误: 工具 '{name}' 不存在"
        try:
            result = await tool["handler"](**kwargs)
            return result
        except Exception as e:
            return f"工具 '{name}' 执行错误: {str(e)}"

    def get_tool_names(self) -> list[str]:
        return list(self._tools.keys())


_registry: ToolRegistry | None = None


def get_tool_registry() -> ToolRegistry:
    global _registry
    if _registry is None:
        _registry = ToolRegistry()
    return _registry
