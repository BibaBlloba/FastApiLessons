from schemas.users import User
from src.models.users import UsersOrm
from src.repos.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User
