import json

from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache

from api.dependencies import DbDep
from schemas.facilities import FacilityAdd
from src.connectors.cache_decorator import custom_cache
from src.init import redis_manager
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Сервисы"])


@router.get("")
@cache(expire=10)  # в секундах
# @custom_cache()
async def get_all_facilities(db: DbDep):
    print("Иду в БД")  # Для дебага
    return await db.facilities.get_all()


@router.post("")
async def create_facility(
    db: DbDep,
    data: FacilityAdd,
):
    await db.facilities.add(data)
    await db.commit()

    test_task.delay()

    raise HTTPException(201)
