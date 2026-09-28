"""学习计划接口：创建、查询、更新、删除。"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.study_plan import StudyPlan
from app.schemas.study_plan import StudyPlanCreate, StudyPlanRead, StudyPlanUpdate

router = APIRouter(tags=["study-plans"])


async def get_plan_or_404(plan_id: int, db: AsyncSession) -> StudyPlan:
    """按 id 取出一条计划；查不到就抛 404。

    查询单个、更新、删除三个接口共用这一处逻辑，避免重复写同样的判断。
    """
    plan = await db.get(StudyPlan, plan_id)
    if plan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学习计划不存在",
        )
    return plan


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


@router.get(
    "/study-plans/{plan_id}",
    response_model=StudyPlanRead,
    summary="查询单个学习计划",
)
async def get_study_plan(
    plan_id: int,
    db: AsyncSession = Depends(get_db),
) -> StudyPlan:
    return await get_plan_or_404(plan_id, db)


@router.patch(
    "/study-plans/{plan_id}",
    response_model=StudyPlanRead,
    summary="更新学习计划",
)
async def update_study_plan(
    plan_id: int,
    payload: StudyPlanUpdate,
    db: AsyncSession = Depends(get_db),
) -> StudyPlan:
    plan = await get_plan_or_404(plan_id, db)

    # exclude_unset=True：只取出前端真正传了的字段，没传的保持原值
    changes = payload.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(plan, field, value)

    # 只改了一个日期时，schema 里的校验看不到另一个日期（它在数据库里），
    # 所以这里用“改完之后”的最终值再检查一次，避免撞上数据库约束报 500
    if plan.start_date and plan.end_date and plan.end_date < plan.start_date:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="结束日期不能早于开始日期",
        )

    await db.commit()
    await db.refresh(plan)
    return plan


@router.delete(
    "/study-plans/{plan_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除学习计划",
)
async def delete_study_plan(
    plan_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    plan = await get_plan_or_404(plan_id, db)

    await db.delete(plan)
    await db.commit()
