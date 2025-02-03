from pydantic import BaseModel
from sqlalchemy import insert, select

from models.users import UsersOrm
from repos.base import BaseRepository
from schemas.user import User


class UsersRepository(BaseRepository):
    model = UsersOrm

    def __init__(self, session) -> None:
        self.session = session

    async def add(self, data: BaseModel):
        stmt = insert(self.model).values(**data.model_dump()).returning()
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()

    async def get_user_with_hashedPwd(self, nickname):
        query = select(self.model).filter_by(nickname=nickname)
        result = await self.session.execute(query)
        result = result.scalars().one()
        return result
