"""ORM 模型（数据表）都放在这个包里。

每新增一个模型文件，都要在这里导入一次：SQLAlchemy 只认识“已经被导入过”的类，
如果漏了这一行，建表时对应的表会被静默忽略。
"""

from app.db.base import Base
from app.models.study_plan import StudyPlan, StudyPlanStatus

__all__ = ["Base", "StudyPlan", "StudyPlanStatus"]
