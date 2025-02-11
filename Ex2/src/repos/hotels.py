from datetime import date

from sqlalchemy import func, insert, select

from models.rooms import RoomsOrm
from repos.utils import rooms_ids_for_booking
from schemas.hotels import Hotel
from src.models.hotels import HotelsOrm
from src.repos.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

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
