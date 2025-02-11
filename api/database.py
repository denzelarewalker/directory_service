from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)


DATABASE_URL = "postgresql+asyncpg://user:password@db/postgres"


async_engine = create_async_engine(DATABASE_URL, echo=True, future=True)


new_session = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass

async def create_tables():
    async with async_engine.begin() as conn:  # Используем async_engine для создания таблиц
        await conn.run_sync(Base.metadata.create_all)  # Создаем все таблицы
