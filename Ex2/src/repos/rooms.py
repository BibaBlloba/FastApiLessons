from datetime import date

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import delete, func, insert, select, update

from src.database import engine
from src.repos.utils import rooms_ids_for_booking
from schemas.rooms import Room
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.repos.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_by_time(
        self,
        hotel_id,
        date_from: date,
        date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))
