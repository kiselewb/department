import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config.settings import settings
from app.database.session import get_session_db
from app.main import app
from app.models.base import Base


engine_test = create_async_engine(settings.TEST_DB_URL, poolclass=NullPool)
async_session_factory_test = async_sessionmaker(
    bind=engine_test, expire_on_commit=False, class_=AsyncSession
)


@pytest.fixture(autouse=True, scope="session")
async def setup_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def session():
    async with async_session_factory_test() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
async def client(session: AsyncSession):
    async def override_get_session():
        yield session

    app.dependency_overrides[get_session_db] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
