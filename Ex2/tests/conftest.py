import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from config import settings
from src.database import Base, engine_null_pool
from src.models import *


@pytest.fixture(autouse=True, scope="session")
async def async_engine():
    assert settings.MODE == "TEST"  # Чтобы убедиться, что находимся в тестовой среде

    async with engine_null_pool.begin() as conn:  # null_pull нужен чтобы не было ошибок с подключениями к БД
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
