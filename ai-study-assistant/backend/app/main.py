"""FastAPI 应用入口：创建应用、注册中间件与路由。"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.db.session import engine, init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """应用启动时初始化数据库，关闭时释放数据库连接。"""
    await init_db()
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

# 允许前端（Vite 开发服务器）访问本服务
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/", tags=["meta"])
async def root() -> dict[str, str]:
    """根路径：确认服务已启动，并给出接口文档地址。"""
    return {
        "message": f"{settings.app_name} is running",
        "docs": "/docs",
    }
