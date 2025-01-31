from pydantic import BaseModel
from sqlalchemy import insert, select


class BaseRepository:
    model = None

    def __init__(self, session) -> None:
        self.session = session

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        stmt = insert(self.model).values(**data.model_dump())
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()
