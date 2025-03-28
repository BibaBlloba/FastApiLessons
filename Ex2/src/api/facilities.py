from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache

from api.dependencies import DbDep
from schemas.facilities import FacilityAdd
from src.tasks.tasks import test_task

router = APIRouter(prefix='/facilities', tags=['Сервисы'])


@router.get('')
@cache(expire=10)  # в секундах
# @custom_cache()
async def get_all_facilities(db: DbDep):
    print('Иду в БД')  # Для дебага
    return await db.facilities.get_all()


@router.post('')
async def create_facility(
    db: DbDep,
    data: FacilityAdd,
):
    result = await db.facilities.add(data)
    await db.commit()

    test_task.delay()

    return JSONResponse(status_code=201, content=result.json())
