import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import settings
from src.database import Base, engine_null_pool
from src.main import app
from src.models import *


@pytest.fixture(autouse=True, scope="session")
async def setup_database():
    assert settings.MODE == "TEST"  # Чтобы убедиться, что находимся в тестовой среде

    async with engine_null_pool.begin() as conn:  # null_pull нужен чтобы не было ошибок с подключениями к БД
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(autouse=True, scope="session")
async def register_user(setup_database):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        response = await ac.post(
            "/auth/register",
            json={
                "email": "example@user.com",
                "password": "123",
                "first_name": "John",
                "last_name": "Pork",
                "login": "Akeka",
            },
        )
        assert response
        print(response.json())
