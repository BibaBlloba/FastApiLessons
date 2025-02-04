from repos.hotels import HotelsRepository
from repos.rooms import RoomsRepository
from repos.users import UsersRepository


class DbManager:
    def __init__(self, session_factory) -> None:
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        """Репозитории"""
        self.hotels = HotelsRepository(self.session)
        self.rooms = RoomsRepository(self.session)
        self.users = UsersRepository(self.session)

        return self

    async def __aexit__(self, *args):  # *args для обработки ошибок
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
