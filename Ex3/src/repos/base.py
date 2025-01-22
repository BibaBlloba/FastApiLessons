from pydantic import BaseModel
from sqlalchemy import insert, select

from src.database import Base


class BaseRepository:
    model = Base

    def __init__(self, session) -> None:
        self.session = session

    async def get_by_id(
        self,
        **filter_by,
    ):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one()

    async def add(self, data: BaseModel):
        stmt = insert(self.model).values(data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().one()

    async def get_all(self, **filter_by):
        pass

    async def edit(self, hotels_data, **filter_by):
        pass

    async def delete(self, **filter_by):
        pass
