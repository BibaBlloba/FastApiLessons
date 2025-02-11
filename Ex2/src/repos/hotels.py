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

    # async def get_all(
    #     self,
    #     location,
    #     title,
    #     limit,
    #     offset,
    # ):
    #     query = select(HotelsOrm)
    #     if location:
    #         query = query.filter(
    #             func.lower(HotelsOrm.location).contains(location.strip().lower())
    #         )
    #     if title:
    #         query = query.filter(
    #             func.lower(HotelsOrm.title).contains(title.strip().lower())
    #         )
    #     query = query.limit(limit).offset(offset)
    #
    #     result = await self.session.execute(query)
    #
    #     return [
    #         self.schema.model_validate(hotel, from_attributes=True)
    #         for hotel in result.scalars().all()
    #     ]

    async def get_by_time(
        self,
        date_from: date,
        date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)

        hotels_ids = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        return await self.get_filtered(self.model.id.in_(hotels_ids))
