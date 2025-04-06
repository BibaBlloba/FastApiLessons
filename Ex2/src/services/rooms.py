from datetime import date

from exceptions import ObjectNotFoundException, WrongDate
from schemas.facilities import RoomsFacilityAdd
from schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest
from src.services.base import BaseService


class RoomsService(BaseService):
    async def get_rooms(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        if date_from > date_to:
            raise WrongDate
        return await self.db.rooms.get_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_room_by_id(
        self,
        hotel_id: int,
        room_id: int,
    ):
        try:
            result = await self.db.rooms.get_one(id=room_id, hotel_id=hotel_id)
        except ObjectNotFoundException:
            raise ObjectNotFoundException
        return result

    async def add_room(
        self,
        hotel_id: int,
        data: RoomAddRequest,
    ):
        _room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
        try:
            result = await self.db.rooms.add(_room_data)
        except ObjectNotFoundException:
            raise ObjectNotFoundException

        if data.facilities_ids:
            rooms_facilities_data = [
                RoomsFacilityAdd(room_id=result.id, facility_id=f_id)
                for f_id in data.facilities_ids
            ]
            await self.db.rooms_facilities.add_bulk(rooms_facilities_data)

        await self.db.commit()
        return result

    async def put_room(
        self,
        hotel_id: int,
        room_id: int,
        data: RoomAddRequest,
    ):
        _room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
        try:
            result = await self.db.rooms.edit(_room_data, id=room_id, hotel_id=hotel_id)
        except ObjectNotFoundException:
            raise ObjectNotFoundException

        await self.db.rooms_facilities.set_facilities(
            room_id=room_id, facilities_ids=data.facilities_ids
        )
        await self.db.commit()
        return result

    async def patch_room(
        self,
        hotel_id: int,
        room_id: int,
        data: RoomPatchRequest,
    ):
        _room_data_dict = data.model_dump(exclude_unset=True)
        _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)

        try:
            result = await self.db.rooms.edit(
                _room_data,
                exclude_unset=True,
                hotel_id=hotel_id,
                id=room_id,
            )
        except ObjectNotFoundException:
            raise ObjectNotFoundException

        if 'facilities_ids' in _room_data_dict:
            await self.db.rooms_facilities.set_facilities(
                room_id=room_id, facilities_ids=_room_data_dict.get('facilities_ids')
            )

        await self.db.commit()
        return result

    async def delete_room(
        self,
        hotel_id: int,
        room_id: int,
    ):
        result = await self.db.rooms.delete(hotel_id=hotel_id, id=room_id)
        await self.db.commit()
        return result
