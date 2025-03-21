import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from os import getenv
from dotenv import load_dotenv
from src.main import app
from src.database.session import Base, get_session

# Загрузка переменных окружения
load_dotenv()
POSTGRES_USER = getenv('TEST_POSTGRES_USER')
POSTGRES_PASS = getenv('TEST_POSTGRES_PASSWORD')
POSTGRES_HOST = getenv('TEST_POSTGRES_HOST')
POSTGRES_PORT = getenv('TEST_POSTGRES_PORT')
POSTGRES_DB = getenv('TEST_POSTGRES_DB')

TEST_DB_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASS}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

@pytest_asyncio.fixture
async def test_db_session():
    engine = create_async_engine(TEST_DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Создание тестовой сессии
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

    # Очистка таблиц после тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def client(test_db_session):
    # Переопределение зависимости get_session для тестов
    app.dependency_overrides[get_session] = lambda: test_db_session

    # Используем AsyncClient для отправки запросов
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client