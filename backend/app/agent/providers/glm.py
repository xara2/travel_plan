"""智谱GLM provider via zhipuai API."""
import os
from typing import AsyncIterator
from .base import BaseLLMProvider


class GLMProvider(BaseLLMProvider):
    def __init__(self):
        self.api_key = os.environ.get("GLM_API_KEY", "")
        self.model = "glm-4"
        self.embed_model = "embedding-2"

    async def chat(self, messages, temperature=0.7, max_tokens=2000):
        from zhipuai import ZhipuAI

        client = ZhipuAI(api_key=self.api_key)
        resp = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content

    async def chat_stream(self, messages, temperature=0.7, max_tokens=2000):
        from zhipuai import ZhipuAI

        client = ZhipuAI(api_key=self.api_key)
        resp = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )
        for chunk in resp:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def embed(self, texts):
        from zhipuai import ZhipuAI

        client = ZhipuAI(api_key=self.api_key)
        resp = client.embeddings.create(
            model=self.embed_model,
            input=texts,
        )
        return [d.embedding for d in resp.data]
