from datetime import date, datetime

from fastapi import APIRouter, Body, HTTPException, Query
from fastapi_cache.decorator import cache

from src.exceptions import ObjectNotFoundException
from src.services.hotels import HotelService
from src.api.dependencies import DbDep, PaginationDap
from src.schemas.hotels import HotelAdd, HotelPATCH

router = APIRouter(prefix='/hotels', tags=['Отели'])


# GET
@cache(expire=10)
@router.get(
    '',
    summary='Получение отелей',
    description='<h1>Развернутое описание</h1>',
)
async def get_hotels(
    pagination: PaginationDap,
    db: DbDep,
    location: str | None = Query(default=None),
    title: str | None = Query(default=None),
    date_from: date = Query(example='2024-08-01'),
    date_to: date = Query(example='2024-08-10'),
):
    hotels = await HotelService(db).get_hotels(
        pagination=pagination,
        location=location,
        title=title,
        date_from=date_from,
        date_to=date_to,
    )
    return hotels


@router.get('/{hotel_id}')
async def get_hotel_by_id(db: DbDep, hotel_id: int):
    try:
        return await HotelService(db).get_hotel_by_id(hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(404, detail='Отель не найден')


# POST
@router.post('')
async def create_hotel(
    db: DbDep,
    hotels_data: HotelAdd = Body(
        openapi_examples={
            '1': {
                'summary': 'Сочи Пример',
                'value': {
                    'title': 'Отель Соич',
                    'location': 'Улица шейха 2',
                },
            },
            '2': {
                'summary': 'Дубай Пример',
                'value': {
                    'title': 'Отель Дубай',
                    'location': 'Улица Дубая 4',
                },
            },
        }
    ),
):
    return await HotelService(db).create_hotel(hotels_data=hotels_data)


# PUT
@router.put('/{hotel_id}')
async def put_hotel(
    hotel_id: int,
    hotels_data: HotelAdd,
    db: DbDep,
):
    return await HotelService(db).edit_hotel(hotels_data=hotels_data, hotel_id=hotel_id)


# PATCH
@router.patch('/{hotel_id}')
async def patch_hotel(
    hotel_id: int,
    hotels_data: HotelPATCH,
    db: DbDep,
):
    return await HotelService(db).patch_hotel(
        hotel_id=hotel_id, hotels_data=hotels_data
    )


# Delete
@router.delete('/{hotel_id}')
async def remove_hotels(
    hotel_id: int,
    db: DbDep,
):
    return await HotelService(db).del_hotel(hotel_id=hotel_id)
