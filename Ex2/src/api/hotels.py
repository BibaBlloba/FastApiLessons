from select import select

from fastapi import APIRouter, Body, Query
from sqlalchemy import insert

from repos.hotels import HotelsRepository
from src.api.dependencies import DbDep, PaginationDap
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.schemas.hotels import HotelAdd, HotelPATCH

router = APIRouter(prefix="", tags=["Отели"])


# GET
@router.get(
    "/hotels",
    summary="Получение отелей",
    description="<h1>Развернутое описание</h1>",
)
async def get_hotels(
    pagination: PaginationDap,
    db: DbDep,
    location: str | None = Query(default=None),
    title: str | None = Query(default=None),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1),
    )


@router.get("/hotels/{hotel_id}")
async def get_hotel_by_id(db: DbDep, hotel_id: int):
    return await db.hotels.get_one_or_none(id=hotel_id)


# POST
@router.post("/hotels")
async def create_hotel(
    db: DbDep,
    hotels_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи Пример",
                "value": {
                    "title": "Отель Соич",
                    "location": "Улица шейха 2",
                },
            },
            "2": {
                "summary": "Дубай Пример",
                "value": {
                    "title": "Отель Дубай",
                    "location": "Улица Дубая 4",
                },
            },
        }
    ),
):
    result = await db.hotels.add(hotels_data)
    await db.commit()
    return {"status": "ok", "data": result}


# PUT
@router.put("/hotel/{hotel_id}")
async def put_hotel(
    hotel_id: int,
    hotels_data: HotelAdd,
    db: DbDep,
):
    await db.hotels.edit(hotels_data, id=hotel_id)
    return {"status": "ok"}


# PATCH
@router.patch("/hotel/{hotel_id}")
async def patch_hotel(
    hotel_id: int,
    hotels_data: HotelPATCH,
    db: DbDep,
):
    await db.hotels.edit(hotels_data, exclude_unset=True, id=hotel_id)
    return {"status": "ok"}


# Delete
@router.delete("/hotel/{hotel_id}")
async def remove_hotels(
    hotel_id: int,
    db: DbDep,
):
    await db.hotels.delete(id=hotel_id)
    return {"status": "ok"}
