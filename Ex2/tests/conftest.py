# ruff: noqa: E402
# ruff: noqa: F403
import json
from unittest import mock


def empty_cache(*args, **kwargs):
    def wrapper(func):
        return func

    return wrapper


mock.patch('fastapi_cache.decorator.cache', lambda *args, **kwargs: lambda f: f).start()

import pytest
from httpx import ASGITransport, AsyncClient

from api.dependencies import get_db
from schemas.hotels import HotelAdd
from schemas.rooms import RoomAdd
from src.config import settings
from src.database import Base, async_session_maker_null_pool, engine_null_pool
from src.main import app
from src.models import *
from src.utils.db_manager import DbManager


async def get_db_null_pull():
    async with DbManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture()
async def db():
    async for db in get_db_null_pull():
        yield db


app.dependency_overrides[get_db] = get_db_null_pull


@pytest.fixture(autouse=True, scope='session')
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://localhost:8000'
    ) as ac:
        yield ac


@pytest.fixture(autouse=True, scope='session')
async def setup_database():
    assert settings.MODE == 'TEST'  # Чтобы убедиться, что находимся в тестовой среде

    async with (
        engine_null_pool.begin() as conn
    ):  # null_pull нужен чтобы не было ошибок с подключениями к БД
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open('tests/mock_data/mock_hotels.json', encoding='utf-8') as file_hotels:
        hotels = json.load(file_hotels)
    with open('tests/mock_data/mock_rooms.json', encoding='utf-8') as file_rooms:
        rooms = json.load(file_rooms)

    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
    rooms = [RoomAdd.model_validate(room) for room in rooms]

    async with DbManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()


@pytest.fixture(autouse=True, scope='session')
async def register_user(setup_database, ac):
    response = await ac.post(  # noqa
        '/auth/register',
        json={
            'email': 'example@user.com',
            'password': '123',
            'first_name': 'John',
            'last_name': 'Pork',
            'login': 'Akeka',
        },
    )


@pytest.fixture(autouse=True)
async def authenticated_ac(ac, register_user):
    response = await ac.post(
        '/auth/login',
        json={
            'email': 'example@user.com',
            'password': '123',
        },
    )
    assert response.status_code == 200
    token = response.cookies.get('access_token', None)
    assert token
    # ac.headers.update({"Authorization": f"Bearer {token}"})
    yield ac
