from datetime import date

from fastapi import APIRouter, HTTPException, Query

from api.dependencies import DbDep
from schemas.facilities import RoomsFacilityAdd
from schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    db: DbDep,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    return await db.rooms.get_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room_by_id(
    hotel_id: int,
    room_id: int,
    db: DbDep,
):
    result = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    print(result)
    return result


@router.post("/{hotel_id}/rooms")
async def add_room(
    hotel_id: int,
    data: RoomAddRequest,
    db: DbDep,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())

    result = await db.rooms.add(_room_data)

    rooms_facilities_data = [
        RoomsFacilityAdd(room_id=result.id, facility_id=f_id)
        for f_id in data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)

    await db.commit()
    return result


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_room(
    hotel_id: int,
    room_id: int,
    data: RoomAddRequest,
    db: DbDep,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    result = await db.rooms.edit(_room_data, id=room_id, hotel_id=hotel_id)

    await db.rooms_facilities.set_facilities(
        room_id=room_id, facilities_ids=data.facilities_ids
    )

    await db.commit()
    raise HTTPException(status_code=201)


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(
    hotel_id: int,
    room_id: int,
    data: RoomPatchRequest,
    db: DbDep,
):
    _room_data_dict = data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)

    await db.rooms.edit(
        _room_data,
        exclude_unset=True,
        hotel_id=hotel_id,
        id=room_id,
    )

    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_facilities(
            room_id=room_id, facilities_ids=_room_data_dict.get("facilities_ids")
        )

    await db.commit()

    raise HTTPException(status_code=201)


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    hotel_id: int,
    room_id: int,
    db: DbDep,
):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    raise HTTPException(status_code=200, detail="Отель удален.")
