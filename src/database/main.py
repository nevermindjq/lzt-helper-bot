import os
from argparse import ArgumentError
from urllib.parse import quote_plus
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine
)

def create_engine() -> AsyncEngine:
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_DATABASE = os.getenv('DB_DATABASE', 'postgres')

    if not all([DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD, DB_DATABASE]):
        raise ArgumentError(
            [DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD, DB_DATABASE],
            'One of environment variables is not set or set incorrectly: DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD, DB_DATABASE'
        )

    return create_async_engine(
        f'postgresql+asyncpg://{DB_USERNAME}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}',
        echo=False,
        pool_size=100,
        max_overflow=100,
        pool_timeout=30,
        pool_recycle=1800,
        pool_pre_ping=True,
    )

def create_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )