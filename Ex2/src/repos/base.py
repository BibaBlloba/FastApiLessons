from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update

from schemas.hotels import Hotel
from src.database import Base


class BaseRepository:
    model = Base
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return [
            self.schema.model_validate(model, from_attributes=True)
            for model in result.scalars().all()
        ]

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        res = result.scalars().one_or_none()
        if res is None:
            return None
        return self.schema.validate(res)

    async def add(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        try:
            result = await self.session.execute(add_data_stmt)
        except:
            raise HTTPException(401, "Пользователь уже зарегестрирован.")
        model = result.scalars().one()
        return self.schema.validate(model)

    async def edit(
        self,
        data: BaseModel,
        exclude_unset: bool = False,
        **filter_by,
    ) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_stmt)

    async def delete_by_id(self, **filter_by) -> None:
        pass

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
