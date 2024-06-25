from collections.abc import AsyncGenerator

from conf.config import settings
from sqlalchemy import QueuePool
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine


def create_engine() -> AsyncEngine:
    return create_async_engine(
        settings.DB_URL,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=20,
        pool_recycle=3600,
    )


def create_session(engine: AsyncEngine | None = None) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine or create_engine(),
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )


engine = create_engine()
async_session = create_session(engine)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
