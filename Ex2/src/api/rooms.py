from fastapi import APIRouter, HTTPException

from repos.rooms import RoomsRepository
from schemas.rooms import RoomAdd, RoomPATCH
from src.database import async_session_maker

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(hotel_id=hotel_id)


@router.post("/rooms")
async def add_room(
    data: RoomAdd,
):
    async with async_session_maker() as session:
        result = await RoomsRepository(session).add(data)
        await session.commit()
        return result


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room_by_id(
    hotel_id: int,
    room_id: int,
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(
            hotel_id=hotel_id, id=room_id
        )


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_room(
    hotel_id: int,
    room_id: int,
    data: RoomAdd,
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data, hotel_id=hotel_id, id=room_id)
        await session.commit()
        raise HTTPException(status_code=201)


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(
    hotel_id: int,
    room_id: int,
    data: RoomPATCH,
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(
            data,
            exclude_unset=True,
            hotel_id=hotel_id,
            id=room_id,
        )
        await session.commit()
        raise HTTPException(status_code=201)


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    hotel_id: int,
    room_id: int,
):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()
        raise HTTPException(status_code=200, detail="Отель удален.")
