from pydantic import EmailStr
from sqlalchemy import select

from schemas.users import User, UserHashedPwd
from src.models.users import UsersOrm
from src.repos.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def get_uesr_with_hashedPwd(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        res = result.scalars().one()
        return UserHashedPwd.validate(res)
