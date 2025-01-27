from fastapi import APIRouter, Body

from repos.users import UsersRepository
from schemas.users import UserRequestAdd
from src.database import async_session_maker

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/regisger")
async def register_user(
    data: UserRequestAdd = Body(
        openapi_examples={
            "1": {
                "summary": "John Pork",
                "value": {
                    "email": "a@a.com",
                    "password": "123",
                    "first_name": "John",
                    "last_name": "Pork",
                    "login": "Akeka",
                },
            },
            "2": {
                "summary": "Админ",
                "value": {
                    "email": "admin@a.com",
                    "password": "123",
                    "first_name": "Админ",
                    "last_name": "Виталя",
                    "login": "admin",
                },
            },
        }
    ),
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).add(data)
        await session.commit()

        return {"status": "ok", "data": data}
