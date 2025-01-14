from fastapi import APIRouter, Body, FastAPI, Query
from sqlalchemy import insert, select

from src.api.dependencies import PaginationDap
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "location": "sochi"},
    {"id": 2, "title": "Дубай", "location": "dubai"},
    {"id": 3, "title": "Мальдивы", "location": "maldivi"},
    {"id": 4, "title": "Геленджик", "location": "gelendzhik"},
    {"id": 5, "title": "Москва", "location": "moscow"},
    {"id": 6, "title": "Казань", "location": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "location": "spb"},
]


# GET
@router.get(
    "/hotels",
    summary="Получение отелей",
    description="<h1>Развернутое описание</h1>",
)
async def get_hotels(
    pagination: PaginationDap,
    id: int | None = Query(default=None),
    title: str | None = Query(default=None),
):
    per_page = pagination.per_page or 5

    async with async_session_maker() as session:

        query = select(HotelsOrm)
        if id:
            query = query.filter_by(id=id)
        if title:
            query = query.filter_by(title=title)
        query = query.limit(per_page).offset(per_page * (pagination.page - 1))

        result = await session.execute(query)

        all = result.scalars().all()
        return all


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
        add_hotel_stmt = insert(HotelsOrm).values(**hotels_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()
        return {"status": "ok"}


# PUT
@router.put("/hotel/{hotel_id}")
async def put_hotel(
    hotel_id: int,
    hotels_data: Hotel,
):
    global hotels
    hotels[hotel_id - 1]["title"] = hotels_data.title
    hotels[hotel_id - 1]["location"] = hotels_data.location
    return {"status": "ok"}


# PATCH
@router.patch("/hotel/{hotel_id}")
async def patch_hotel(
    hotel_id: int,
    hotels_data: HotelPATCH,
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotels_data.title is not None:
        hotel["title"] = hotels_data.title
    if hotels_data.location is not None:
        hotel["location"] = hotels_data.location
    return hotel
