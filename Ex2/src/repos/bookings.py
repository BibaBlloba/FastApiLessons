from datetime import date

from pydantic import BaseModel
from sqlalchemy import insert, select

from repos.utils import rooms_ids_for_booking
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.repos.base import BaseRepository
from src.repos.mappers.mappers import BookingsDataMapper


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingsDataMapper

    async def get_bookings_with_today_checkin(self):
        query = select(BookingsOrm).filter(BookingsOrm.date_from == date.today())
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(booking)
            for booking in result.scalars().all()
        ]

    async def add(self, data: BaseModel, hotel_id: int):
        query = rooms_ids_for_booking(
            date_from=data.date_from,
            date_to=data.date_to,
            hotel_id=hotel_id,
        )
        rooms_ids_to_get = await self.session.execute(query)
        rooms_ids_to_get = rooms_ids_to_get.scalars().all()
        print(rooms_ids_to_get)
        if data.room_id not in rooms_ids_to_get:
            raise ValueError

        add_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)
