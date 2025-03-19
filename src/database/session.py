from os import getenv
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
POSTGRES_USER = getenv('POSTGRES_USER')
POSTGRES_PASS = getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = getenv('POSTGRES_HOST')
POSTGRES_PORT = getenv('POSTGRES_PORT')
POSTGRES_DB = getenv('POSTGRES_DB')

# Настройки подключения к БД
DB_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASS}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Инициализация движка и сессии
engine = create_async_engine(DB_URL, echo=True)
async_session = sessionmaker(engine,
                             class_=AsyncSession,
                             expire_on_commit=False)

# База для моделей
Base = declarative_base()


async def init_db():
    """
    Инициализация БД: создание таблиц, если их нет.
    """
    async with engine.begin() as conn:
        # Создаем все таблицы, если они еще не существуют
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Генератор сессий для Dependency Injection.
    """
    async with async_session() as session:
        yield session
