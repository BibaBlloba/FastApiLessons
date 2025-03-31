from datetime import date, datetime

from fastapi import APIRouter, Body, HTTPException, Query
from fastapi_cache.decorator import cache

from exceptions import ObjectNotFoundException
from src.api.dependencies import DbDep, PaginationDap
from src.schemas.hotels import HotelAdd, HotelPATCH

router = APIRouter(prefix='', tags=['Отели'])


# GET
@cache(expire=10)
@router.get(
    '/hotels',
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
    if date_from > date_to:
        raise HTTPException(404, 'Неверная дата')
    per_page = pagination.per_page or 5
    return await db.hotels.get_by_time(
        location=location,
        title=title,
        date_from=date_from,
        date_to=date_to,
        limit=per_page,
        offset=per_page * (pagination.page - 1),
    )


@router.get('/hotels/{hotel_id}')
async def get_hotel_by_id(db: DbDep, hotel_id: int):
    try:
        result = await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(404, detail='Отель не найден')
    return result


# POST
@router.post('/hotels')
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
    result = await db.hotels.add(hotels_data)
    await db.commit()
    return {'status': 'ok', 'data': result}


# PUT
@router.put('/hotel/{hotel_id}')
async def put_hotel(
    hotel_id: int,
    hotels_data: HotelAdd,
    db: DbDep,
):
    await db.hotels.edit(hotels_data, id=hotel_id)
    return {'status': 'ok'}


# PATCH
@router.patch('/hotel/{hotel_id}')
async def patch_hotel(
    hotel_id: int,
    hotels_data: HotelPATCH,
    db: DbDep,
):
    result = await db.hotels.edit(hotels_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return result


# Delete
@router.delete('/hotel/{hotel_id}')
async def remove_hotels(
    hotel_id: int,
    db: DbDep,
):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {'status': 'ok'}
