import json

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine

from schemas.hotels import HotelAdd
from schemas.rooms import RoomAdd
from src.config import settings
from src.database import Base, async_session_maker_null_pool, engine_null_pool
from src.main import app
from src.models import *
from src.utils.db_manager import DbManager


@pytest.fixture(autouse=True, scope="session")
async def setup_database():
    assert settings.MODE == "TEST"  # Чтобы убедиться, что находимся в тестовой среде

    async with engine_null_pool.begin() as conn:  # null_pull нужен чтобы не было ошибок с подключениями к БД
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_data/mock_hotels.json") as f:
        data = json.load(f)
        for object in data:
            object_data = HotelAdd(**object)
            async with DbManager(session_factory=async_session_maker_null_pool) as db:
                new_hotel_data = await db.hotels.add(object_data)
                await db.commit()
                assert new_hotel_data

    with open("tests/mock_data/mock_rooms.json") as f:
        data = json.load(f)
        for object in data:
            object_data = RoomAdd(**object)
            async with DbManager(session_factory=async_session_maker_null_pool) as db:
                new_hotel_data = await db.rooms.add(object_data)
                await db.commit()
                assert new_hotel_data


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
