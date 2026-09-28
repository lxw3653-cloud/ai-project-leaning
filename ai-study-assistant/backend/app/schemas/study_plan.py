"""学习计划接口的请求与响应结构。"""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.study_plan import StudyPlanStatus


class StudyPlanCreate(BaseModel):
    """创建学习计划时的请求体。

    这个结构决定前端“能传什么”，例如 id、创建时间不允许前端指定，
    所以它们只出现在下面的 StudyPlanRead 里。
    """

    title: str = Field(
        min_length=1,
        max_length=200,
        description="计划标题，必填",
    )
    description: str | None = Field(default=None, description="计划描述")
    status: StudyPlanStatus = Field(
        default=StudyPlanStatus.NOT_STARTED,
        description="计划状态，不传则默认为 not_started",
    )
    start_date: date | None = Field(default=None, description="开始日期")
    end_date: date | None = Field(default=None, description="结束日期")

    @model_validator(mode="after")
    def check_date_order(self) -> "StudyPlanCreate":
        """日期先后由接口层先拦一道。

        数据库里也有同样的 CHECK 约束，但那条约束触发时只会报服务端错误，
        在这里校验可以返回 422 和清楚的提示信息。
        """
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("结束日期不能早于开始日期")
        return self


class StudyPlanRead(BaseModel):
    """返回给前端的学习计划结构。"""

    # from_attributes 允许直接把 SQLAlchemy 的对象转成这个结构
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: StudyPlanStatus
    start_date: date | None
    end_date: date | None
    created_at: datetime
    updated_at: datetime
