from datetime import date
from fastapi import HTTPException
from src.schemas.hotels import HotelAdd
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_hotels(
        self,
        pagination,
        location: str | None,
        title: str | None,
        date_from: date,
        date_to: date,
    ):
        if date_from > date_to:
            raise HTTPException(404, 'Неверная дата')
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_by_time(
            location=location,
            title=title,
            date_from=date_from,
            date_to=date_to,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

    async def get_hotel_by_id(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def create_hotel(self, hotels_data: HotelAdd):
        result = await self.db.hotels.add(hotels_data)
        await self.db.commit()
        return {'status': 'ok', 'data': result}

    async def edit_hotel(self, hotels_data: HotelAdd, hotel_id: int):
        await self.db.hotels.edit(hotels_data, id=hotel_id)
        return {'status': 'ok'}

    async def patch_hotel(self, hotel_id: int, hotels_data: HotelAdd):
        result = await self.db.hotels.edit(hotels_data, exclude_unset=True, id=hotel_id)
        await self.db.commit()
        return result

    async def del_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
        return {'status': 'ok'}
