import json

from fastapi import APIRouter, HTTPException

from api.dependencies import DbDep
from schemas.facilities import FacilityAdd
from src.init import redis_manager

router = APIRouter(prefix="/facilities", tags=["Сервисы"])


@router.get("")
async def get_all_facilities(db: DbDep):
    facilities_from_cache = await redis_manager.get("facilities")
    print(f"{facilities_from_cache=}")

    if not facilities_from_cache:
        facilities = await db.facilities.get_all()
        facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schemas)
        await redis_manager.set("facilities", facilities_json, expire=10)

        return facilities

    facilities_dicts = json.loads(facilities_from_cache)
    return facilities_dicts


@router.post("")
async def create_facility(
    db: DbDep,
    data: FacilityAdd,
):
    await db.facilities.add(data)
    await db.commit()
    raise HTTPException(201)
