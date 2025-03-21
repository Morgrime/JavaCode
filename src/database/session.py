from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (AsyncSession,
                                    create_async_engine,
                                    async_sessionmaker)
# from sqlalchemy.orm import sessionmaker

from database.config import settings
from models.wallet_model import Base

# Инициализация движка и сессии
engine = create_async_engine(url=settings.DATABASE_URL_asyncpg, echo=True)
async_session = async_sessionmaker(engine,
                                   class_=AsyncSession,
                                   expire_on_commit=False)


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
