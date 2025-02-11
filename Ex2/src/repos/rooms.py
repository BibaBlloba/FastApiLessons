from datetime import date

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import delete, func, insert, select, update

from database import engine
from repos.utils import rooms_ids_for_booking
from schemas.rooms import Room
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.repos.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(self, **filter_by_hotel):
        query = select(self.model).filter_by(**filter_by_hotel)
        result = await self.session.execute(query)
        result_array = result.scalars().all()
        if not result_array:
            raise HTTPException(status_code=404, detail="Отель пустой не найден.")
        return [
            self.schema.model_validate(model, from_attributes=True)
            for model in result_array
        ]

    async def add(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        try:
            result = await self.session.execute(add_data_stmt)
        except:
            raise HTTPException(404, "Такого отеля не существует.")
        model = result.scalars().one()
        return self.schema.validate(model)

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
