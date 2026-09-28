"""数据库引擎与会话工厂（当前只做规划，没有任何数据表）。

等确认第一个业务功能之后，再在这里补充建表逻辑，或引入 Alembic 做数据库迁移。
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

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


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """供 FastAPI 依赖注入使用的数据库会话。

    将来这样使用：

        @router.get("/items")
        async def list_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        yield session
