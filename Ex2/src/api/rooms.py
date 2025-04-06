from datetime import date

from fastapi import APIRouter, HTTPException, Query

from api.dependencies import DbDep
from exceptions import ObjectNotFoundException, WrongDate
from schemas.rooms import RoomAddRequest, RoomPatchRequest
from services.rooms import RoomsService

router = APIRouter(prefix='/hotels', tags=['Номера'])


@router.get('/{hotel_id}/rooms')
async def get_rooms(
    hotel_id: int,
    db: DbDep,
    date_from: date = Query(example='2024-08-01'),
    date_to: date = Query(example='2024-08-10'),
):
    try:
        return await RoomsService(db).get_rooms(hotel_id, date_from, date_to)
    except WrongDate as ex:
        raise HTTPException(404, ex.detail)


@router.get('/{hotel_id}/rooms/{room_id}')
async def get_room_by_id(
    hotel_id: int,
    room_id: int,
    db: DbDep,
):
    try:
        return await RoomsService(db).get_room_by_id(hotel_id, room_id)
    except ObjectNotFoundException:
        raise HTTPException(404, detail='Номер не найден')


@router.post('/{hotel_id}/rooms')
async def add_room(
    hotel_id: int,
    data: RoomAddRequest,
    db: DbDep,
):
    try:
        return await RoomsService(db).add_room(hotel_id, data)
    except ObjectNotFoundException:
        raise HTTPException(404, detail='Отель не найден')


@router.put('/{hotel_id}/rooms/{room_id}')
async def put_room(
    hotel_id: int,
    room_id: int,
    data: RoomAddRequest,
    db: DbDep,
):
    try:
        return await RoomsService(db).put_room(hotel_id, room_id, data)
    except ObjectNotFoundException:
        raise HTTPException(404, detail='Номер не найден')


@router.patch('/{hotel_id}/rooms/{room_id}')
async def patch_room(
    hotel_id: int,
    room_id: int,
    data: RoomPatchRequest,
    db: DbDep,
):
    try:
        return await RoomsService(db).patch_room(hotel_id, room_id, data)
    except ObjectNotFoundException:
        raise HTTPException(404, detail='Номер не найден')


@router.delete('/{hotel_id}/rooms/{room_id}')
async def delete_room(
    hotel_id: int,
    room_id: int,
    db: DbDep,
):
    return await RoomsService(db).patch_room(hotel_id, room_id)
