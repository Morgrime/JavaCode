from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.v1.wallets import main_router
from database.session import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan для инициализации базы данных при старте приложения.
    """
    # Создаем таблицы, если их нет
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield  # Приложение работает

    # Очистка при завершении (если нужно)
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)

app = FastAPI(title="Wallet API",
              description="API для управления кошельками",
              version="1.0.0",
              lifespan=lifespan)
app.include_router(main_router)
