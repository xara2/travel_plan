"""LLM client factory. Returns provider based on LLM_PROVIDER config."""
import os
from dotenv import load_dotenv

# Ensure .env is loaded before reading env vars
_base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_env_path = os.path.join(_base_dir, ".env")
if os.path.exists(_env_path):
    load_dotenv(_env_path)

from .providers.base import BaseLLMProvider
from .providers.qwen import QwenProvider
from .providers.ernie import ErnieProvider
from .providers.glm import GLMProvider

_providers: dict[str, type[BaseLLMProvider]] = {
    "qwen": QwenProvider,
    "ernie": ErnieProvider,
    "glm": GLMProvider,
}


def get_llm_client() -> BaseLLMProvider:
    provider_name = os.environ.get("LLM_PROVIDER", "qwen").lower()
    provider_cls = _providers.get(provider_name)
    if not provider_cls:
        raise ValueError(f"Unknown LLM provider: {provider_name}. Options: {list(_providers.keys())}")
    return provider_cls()
