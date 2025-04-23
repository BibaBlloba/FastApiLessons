from fastapi import HTTPException
from exceptions import AllRoomsAreBooked
from schemas.bookings import BookingAdd
from services.base import BaseService


class BookingsService(BaseService):
    async def create_facility(self, data, user_id):
        room = await self.db.rooms.get_one(id=data.room_id)
        room_price: int = room.price
        hotel = await self.db.hotels.get_one(id=room.hotel_id)
        _data = BookingAdd(
            user_id=user_id,
            price=room_price,
            **data.model_dump(),
        )
        try:
            result = await self.db.bookings.add(_data, hotel_id=hotel.id)
        except AllRoomsAreBooked as ex:
            raise ex
        await self.db.commit()
        return result
