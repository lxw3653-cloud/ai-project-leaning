"""学习计划接口（第一阶段：创建 + 查询列表）。"""

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.study_plan import StudyPlan
from app.schemas.study_plan import StudyPlanCreate, StudyPlanRead

router = APIRouter(tags=["study-plans"])


@router.post(
    "/study-plans",
    response_model=StudyPlanRead,
    status_code=status.HTTP_201_CREATED,
    summary="创建学习计划",
)
async def create_study_plan(
    payload: StudyPlanCreate,
    db: AsyncSession = Depends(get_db),
) -> StudyPlan:
    plan = StudyPlan(**payload.model_dump())

    db.add(plan)
    await db.commit()
    # 提交后刷新，才能拿到数据库生成的 id 和创建/更新时间
    await db.refresh(plan)

    return plan


@router.get(
    "/study-plans",
    response_model=list[StudyPlanRead],
    summary="查询全部学习计划",
)
async def list_study_plans(db: AsyncSession = Depends(get_db)) -> list[StudyPlan]:
    # 新创建的计划排在最前面；以后数据变多再考虑分页
    result = await db.execute(
        select(StudyPlan).order_by(StudyPlan.created_at.desc())
    )
    return list(result.scalars().all())
