from datetime import date

from sqlalchemy import func, select

from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repos.base import BaseRepository
from src.repos.mappers.mappers import HotelDataMapper
from src.repos.utils import rooms_ids_for_booking


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    mapper = HotelDataMapper

    async def get_by_time(
        self,
        date_from: date,
        date_to: date,
        location,
        title,
        limit,
        offset,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)

        hotels_ids = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
            .limit(limit)
            .offset(offset)
        )

        if location:
            hotels_ids = hotels_ids.filter(
                func.lower(HotelsOrm.location).contains(location.strip().lower())
            )
        if title:
            hotels_ids = hotels_ids.filter(
                func.lower(HotelsOrm.title).contains(title.strip().lower())
            )

        return await self.get_filtered(self.model.id.in_(hotels_ids))
