from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update

from schemas.hotels import Hotel
from src.database import Base


class BaseRepository:
    model = Base

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        result = await self.session.execute(add_data_stmt)

        return result.scalars().one()

    async def edit(
        self,
        data: BaseModel,
        **filter_by,
    ) -> None:
        update_stmt = (
            update(self.model).filter_by(**filter_by).values(data.model_dump())
        )
        await self.session.execute(update_stmt)

    async def delete_by_id(self, **filter_by) -> None:
        pass

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
