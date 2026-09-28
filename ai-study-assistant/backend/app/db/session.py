"""数据库引擎、会话工厂与建表逻辑。

这个文件负责“怎么连数据库”，具体的表结构定义在 app/models/ 里。
等表结构稳定后，可以把这里的 create_all 换成 Alembic 做正式的数据库迁移。
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# 这行 import 有副作用：它会加载 app/models 下的所有模型类，
# 把它们登记到 Base.metadata。去掉它，create_all 会认为“没有表需要创建”。
from app import models  # noqa: F401
from app.core.config import DATA_DIR, get_settings
from app.db.base import Base

settings = get_settings()

# 注意：创建引擎不会立刻连接数据库，真正连接发生在第一次执行 SQL 时
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db() -> None:
    """创建所有数据表。

    create_all 是幂等的：表已存在时什么都不做，因此可以安全地在每次启动时调用。
    它不会修改已存在表的结构，所以以后改字段时要么写迁移，要么删掉 app.db 重建。
    """
    # SQLite 只是一个普通文件，它所在的目录必须先存在
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """供 FastAPI 依赖注入使用的数据库会话。

    将来这样使用：

        @router.get("/items")
        async def list_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        yield session
