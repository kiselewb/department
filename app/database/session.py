from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config.settings import settings


engine = create_async_engine(url=settings.DB_URL)
async_session_factory = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


async def get_session_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
