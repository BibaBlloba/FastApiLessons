from pydantic import BaseModel, EmailStr
from sqlalchemy import insert, select

from exceptions import UserAlredyRegistered
from src.models.users import UsersOrm
from src.repos.base import BaseRepository
from src.repos.mappers.mappers import UsersDataMapper


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UsersDataMapper

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
        except Exception:
            raise UserAlredyRegistered
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)
