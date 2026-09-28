"""应用配置：统一管理应用信息、跨域白名单、数据库地址等设置。"""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# 本文件位于 backend/app/core/ 下，parents[2] 即 backend/ 目录
BACKEND_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BACKEND_DIR / "data"


class Settings(BaseSettings):
    """从环境变量或 .env 文件读取配置，未设置时使用下面的默认值。"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "AI Study Assistant API"
    app_version: str = "0.1.0"
    debug: bool = True
    api_prefix: str = "/api"

    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    # SQLite + 异步驱动；数据文件默认放在 backend/data/app.db
    database_url: str = f"sqlite+aiosqlite:///{(DATA_DIR / 'app.db').as_posix()}"

    # ---------------- AI（大模型）配置 ----------------
    # 走 OpenAI 兼容接口，换服务商只需要改这三个值，代码不用动。
    # API Key 只从后端的 .env / 环境变量读取，绝不能出现在前端代码里。
    ai_api_key: str = ""
    ai_base_url: str = "https://api.openai.com/v1"
    ai_model: str = "gpt-4o-mini"
    ai_timeout: float = 60.0


@lru_cache
def get_settings() -> Settings:
    """返回配置单例，避免重复读取 .env 文件。"""
    return Settings()
