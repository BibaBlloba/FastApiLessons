from fastapi import APIRouter, HTTPException

from api.dependencies import DbDep
from schemas.facilities import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Сервисы"])


@router.get("/")
async def get_all_facilities(db: DbDep):
    return await db.facilities.get_all()


@router.post("/")
async def create_facility(
    db: DbDep,
    data: FacilityAdd,
):
    try:
        await db.facilities.add(data)
    except:
        raise HTTPException(
            500, detail="Непредвиденная ошибка на моменте создания сервиса."
        )
    await db.commit()
    raise HTTPException(201)
