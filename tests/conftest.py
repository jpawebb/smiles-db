import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from app.config import database_settings

TEST_DATABASE_URL = database_settings.POSTGRES_URL + "_test"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)

TestingSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_test_database():
    """Create tables before tests and drop after."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session():
    """Provide an isolated async database session for a single test."""
    async with TestingSessionLocal() as session:
        yield session
