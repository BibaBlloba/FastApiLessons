from fastapi import HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import insert, select

from schemas.users import User, UserHashedPwd
from src.models.users import UsersOrm
from src.repos.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def get_uesr_with_hashedPwd(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

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
