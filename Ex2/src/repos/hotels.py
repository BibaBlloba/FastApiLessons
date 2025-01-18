from sqlalchemy import func, insert, select

from src.models.hotels import HotelsOrm
from src.repos.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
        self,
        location,
        title,
        limit,
        offset,
    ):
        query = select(HotelsOrm)
        if location:
            query = query.filter(
                func.lower(HotelsOrm.location).contains(location.strip().lower())
            )
        if title:
            query = query.filter(
                func.lower(HotelsOrm.title).contains(title.strip().lower())
            )
        query = query.limit(limit).offset(offset)

        result = await self.session.execute(query)

        return result.scalars().all()

    async def create_hotel(self, hotels_data):
        add_hotel_stmt = insert(self.model).values(**hotels_data.model_dump())
        await self.session.execute(add_hotel_stmt)

        return hotels_data
