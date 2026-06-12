"""阿里通义千问 provider via DashScope API."""
import os
from typing import AsyncIterator
from .base import BaseLLMProvider


class QwenProvider(BaseLLMProvider):
    def __init__(self):
        self.api_key = os.environ.get("QWEN_API_KEY", "")
        self.model = "qwen-turbo"
        self.embed_model = "text-embedding-v3"

    async def chat(self, messages, temperature=0.7, max_tokens=2000):
        import dashscope
        from http import HTTPStatus

        dashscope.api_key = self.api_key
        resp = dashscope.Generation.call(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            result_format="message",
        )
        if resp.status_code == HTTPStatus.OK:
            return resp.output.choices[0].message.content
        raise Exception(f"Qwen API error: {resp.code} - {resp.message}")

    async def chat_stream(self, messages, temperature=0.7, max_tokens=2000):
        import dashscope
        from http import HTTPStatus

        dashscope.api_key = self.api_key
        resp = dashscope.Generation.call(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            result_format="message",
            stream=True,
            incremental_output=True,
        )
        for chunk in resp:
            if chunk.status_code == HTTPStatus.OK:
                content = chunk.output.choices[0].message.content
                if content:
                    yield content

    async def embed(self, texts):
        import dashscope
        from http import HTTPStatus

        dashscope.api_key = self.api_key
        embeddings = []
        for text in texts:
            resp = dashscope.TextEmbedding.call(
                model=self.embed_model,
                input=text,
            )
            if resp.status_code == HTTPStatus.OK:
                embeddings.append(resp.output.embeddings[0].embedding)
            else:
                raise Exception(f"Qwen embed error: {resp.code} - {resp.message}")
        return embeddings
