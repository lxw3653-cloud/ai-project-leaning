"""ORM 模型基类。

以后定义的每一张表都继承 Base，例如：

    class StudyPlan(Base):
        __tablename__ = "study_plans"
        ...
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
