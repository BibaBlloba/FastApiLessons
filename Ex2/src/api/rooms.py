from fastapi import APIRouter, HTTPException

from api.dependencies import DbDep
from repos.rooms import RoomsRepository
from schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest
from src.database import async_session_maker

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    db: DbDep,
):
    return await db.rooms.get_all(hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def add_room(
    hotel_id: int,
    data: RoomAddRequest,
    db: DbDep,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    result = await db.rooms.add(_room_data)
    await db.commit()
    return result


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room_by_id(
    hotel_id: int,
    room_id: int,
    db: DbDep,
):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_room(
    hotel_id: int,
    room_id: int,
    data: RoomAddRequest,
    db: DbDep,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    await db.rooms.edit(_room_data, id=room_id, hotel_id=hotel_id)
    raise HTTPException(status_code=201)


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(
    hotel_id: int,
    room_id: int,
    data: RoomPatchRequest,
    db: DbDep,
):
    _room_data = RoomPatch(hotel_id=hotel_id, **data.model_dump(exclude_unset=True))
    await db.rooms.edit(
        _room_data,
        exclude_unset=True,
        hotel_id=hotel_id,
        id=room_id,
    )
    raise HTTPException(status_code=201)


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    hotel_id: int,
    room_id: int,
    db: DbDep,
):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    raise HTTPException(status_code=200, detail="Отель удален.")
