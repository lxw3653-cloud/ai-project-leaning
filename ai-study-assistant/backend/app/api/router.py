"""汇总所有子路由，对外只暴露一个 api_router。"""

from fastapi import APIRouter

from app.api.routes import ai, health, study_plans

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(study_plans.router)
api_router.include_router(ai.router)
