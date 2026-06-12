"""百度文心一言 provider via 千帆 API."""
import os
import json
from typing import AsyncIterator
from .base import BaseLLMProvider


class ErnieProvider(BaseLLMProvider):
    def __init__(self):
        self.api_key = os.environ.get("ERNIE_API_KEY", "")
        self.secret_key = os.environ.get("ERNIE_SECRET_KEY", "")
        self.model = "ernie-3.5-8k"
        self.embed_model = "embedding-v1"

    async def _get_access_token(self):
        import httpx
        url = (
            "https://aip.baidubce.com/oauth/2.0/token"
            f"?grant_type=client_credentials"
            f"&client_id={self.api_key}"
            f"&client_secret={self.secret_key}"
        )
        async with httpx.AsyncClient() as client:
            resp = await client.post(url)
            return resp.json()["access_token"]

    async def _call_api(self, messages, temperature=0.7, max_tokens=2000, stream=False):
        import httpx
        token = await self._get_access_token()
        url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{self.model}?access_token={token}"
        payload = {
            "messages": messages,
            "temperature": temperature,
            "max_output_tokens": max_tokens,
            "stream": stream,
        }
        return url, payload

    async def chat(self, messages, temperature=0.7, max_tokens=2000):
        import httpx
        url, payload = await self._call_api(messages, temperature, max_tokens, stream=False)
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(url, json=payload)
            return resp.json()["result"]

    async def chat_stream(self, messages, temperature=0.7, max_tokens=2000):
        import httpx
        url, payload = await self._call_api(messages, temperature, max_tokens, stream=True)
        async with httpx.AsyncClient(timeout=120) as client:
            async with client.stream("POST", url, json=payload) as resp:
                async for line in resp.aiter_lines():
                    if line.startswith("data:"):
                        data = json.loads(line[5:].strip())
                        if data.get("result"):
                            yield data["result"]
                        if data.get("is_end"):
                            break

    async def embed(self, texts):
        import httpx
        token = await self._get_access_token()
        url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/embeddings/{self.embed_model}?access_token={token}"
        embeddings = []
        async with httpx.AsyncClient(timeout=30) as client:
            for text in texts:
                resp = await client.post(url, json={"input": [text]})
                data = resp.json()
                if data.get("data"):
                    embeddings.append(data["data"][0]["embedding"])
                else:
                    raise Exception(f"ERNIE embed error: {data}")
        return embeddings
