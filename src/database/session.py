from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class AsyncDatabase:
    def __init__(self, db_url: str):
        self.engine = create_async_engine(
            db_url,
            future=True,
            echo=False,
            pool_size=20,
            max_overflow=0
        )
        self.async_session = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False
        )

    async def get_session(self) -> AsyncSession:
        async with self.async_session() as session:
            yield session
