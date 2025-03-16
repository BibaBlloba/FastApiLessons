from datetime import date

from sqlalchemy import select

from src.models.bookings import BookingsOrm
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
