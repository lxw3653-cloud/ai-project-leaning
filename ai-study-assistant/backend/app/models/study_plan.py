"""学习计划的数据表模型（对应 study_plans 表）。"""

import enum
from datetime import date, datetime, timezone

from sqlalchemy import CheckConstraint, Date, DateTime, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class StudyPlanStatus(str, enum.Enum):
    """学习计划的状态。

    继承 str 是为了将来序列化成 JSON 时直接得到字符串，
    例如 StudyPlanStatus.NOT_STARTED 会变成 "not_started"。
    """

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


def utc_now() -> datetime:
    """返回当前 UTC 时间（带时区信息）。"""
    return datetime.now(timezone.utc)


class StudyPlan(Base):
    """一条学习计划，对应 study_plans 表里的一行记录。"""

    __tablename__ = "study_plans"

    # 数据完整性约束：结束日期不能早于开始日期（两个日期都填了才校验）
    __table_args__ = (
        CheckConstraint(
            "start_date IS NULL OR end_date IS NULL OR end_date >= start_date",
            name="ck_study_plans_date_order",
        ),
    )

    # 主键，由数据库自增生成
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # 标题必填；描述可以为空
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # 状态只允许取枚举里定义的值。values_callable 让数据库里存的是
    # not_started 这类小写值，而不是 NOT_STARTED 这样的成员名。
    status: Mapped[StudyPlanStatus] = mapped_column(
        Enum(
            StudyPlanStatus,
            name="study_plan_status",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
        default=StudyPlanStatus.NOT_STARTED,
        server_default=StudyPlanStatus.NOT_STARTED.value,
    )

    # 计划的时间范围，先允许为空，由用户自己决定填不填
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    # 创建时间和更新时间由程序自动维护，不需要使用者手动传
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    def __repr__(self) -> str:
        """打印对象时的可读形式，方便调试。"""
        return (
            f"StudyPlan(id={self.id!r}, title={self.title!r}, status={self.status!r})"
        )
