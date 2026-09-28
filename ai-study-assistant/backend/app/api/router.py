"""汇总所有子路由，对外只暴露一个 api_router。"""

from fastapi import APIRouter

from app.api.routes import health

api_router = APIRouter()
api_router.include_router(health.router)
