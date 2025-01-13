from fastapi import APIRouter, Body, FastAPI, Query

from src.api.dependencies import PaginationDap
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
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

    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

        if pagination.page and pagination.per_page:
            return hotels_[pagination.per_page * (pagination.page - 1) :][
                : pagination.per_page
            ]
        return hotels_


# POST
@router.post("/hotels")
async def create_hotel(
    hotels_data: Hotel = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи Пример",
                "value": {
                    "title": "Отель Соич",
                    "name": "otel_sochi",
                },
            },
            "2": {
                "summary": "Дубай Пример",
                "value": {
                    "title": "Отель Дубай",
                    "name": "otel_dubai",
                },
            },
        }
    ),
):
    global hotels
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1,
            "title": hotels_data.title,
            "name": hotels_data.name,
        }
    )
    return {"status": "ok"}


# PUT
@router.put("/hotel/{hotel_id}")
async def put_hotel(
    hotel_id: int,
    hotels_data: Hotel,
):
    global hotels
    hotels[hotel_id - 1]["title"] = hotels_data.title
    hotels[hotel_id - 1]["name"] = hotels_data.name
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
    if hotels_data.name is not None:
        hotel["name"] = hotels_data.name
    return hotel
