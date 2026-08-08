"""Configuration and settings for ORACLE.

Loads environment variables via python-dotenv and exposes a Pydantic
`Settings` instance for application use. Looks for `.env` in repository root
and in the `ai/` folder (where environments and venv are kept).
"""
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import os
from typing import Any

try:
    from langchain_openrouter import ChatOpenRouter
except ImportError:
    ChatOpenRouter = None

try:
    from langchain_openai import ChatOpenAI
except ImportError:
    ChatOpenAI = None

# Load project-level .env and ai/.env (ai folder preferred for developer venv)
load_dotenv(dotenv_path=".env", override=False)
load_dotenv(dotenv_path=os.path.join("ai", ".env"), override=False)


class Settings(BaseSettings):
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str | None = None
    OPENROUTER_API_KEY: str | None = None
    OPENROUTER_MODEL: str | None = None

    class Config:
        env_file = os.path.join("ai", ".env")
        env_file_encoding = "utf-8"


settings = Settings()


def get_chat_model(model: str, temperature: float = 0.7) -> Any:
    """Return a configured chat model for OpenRouter or OpenAI."""
    if settings.OPENROUTER_API_KEY and ChatOpenRouter is not None:
        return ChatOpenRouter(
            api_key=settings.OPENROUTER_API_KEY,
            model=settings.OPENROUTER_MODEL or model,
            temperature=temperature,
        )

    if settings.OPENAI_API_KEY and ChatOpenAI is not None:
        return ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_MODEL or model,
            temperature=temperature,
        )

    return None
