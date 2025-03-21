from select import select

from fastapi import APIRouter, Body, Query
from sqlalchemy import insert

from repos.hotels import HotelsRepository
from src.api.dependencies import PaginationDap
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="", tags=["Отели"])


# GET
@router.get(
    "/hotels",
    summary="Получение отелей",
    description="<h1>Развернутое описание</h1>",
)
async def get_hotels(
    pagination: PaginationDap,
    location: str | None = Query(default=None),
    title: str | None = Query(default=None),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )


@router.get("/hotels/{hotels_id}")
async def get_hotel_by_id(hotels_id: int):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).get_by_id(id=hotels_id)
        return result


# POST
@router.post("/hotels")
async def create_hotel(
    hotels_data: Hotel = Body(
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
    async with async_session_maker() as session:
        result = await HotelsRepository(session).add(hotels_data)

        await session.commit()  # не вносить в репо
        return {"status": "ok", "data": result}


# PUT
@router.put("/hotel/{hotel_id}")
async def put_hotel(
    hotel_id: int,
    hotels_data: Hotel,
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotels_data, id=hotel_id)
        await session.commit()
        return {"status": "ok"}


# PATCH
@router.patch("/hotel/{hotel_id}")
async def patch_hotel(
    hotel_id: int,
    hotels_data: HotelPATCH,
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(
            hotels_data, exclude_unset=True, id=hotel_id
        )
        await session.commit()
        return {"status": "ok"}


# Delete
@router.delete("/hotel/{hotel_id}")
async def remove_hotels(
    hotel_id: int,
):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
        return {"status": "ok"}
