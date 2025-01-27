from fastapi import APIRouter, Body
from passlib.context import CryptContext

from repos.users import UsersRepository
from schemas.users import UserAdd, UserRequestAdd
from src.database import async_session_maker

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
    hashed_password = pwd_context.hash(data.password)
    hashed_user_data = UserAdd(
        first_name=data.first_name,
        last_name=data.last_name,
        login=data.login,
        email=data.email,
        hashed_password=hashed_password,
    )
    async with async_session_maker() as session:
        user = await UsersRepository(session).add(hashed_user_data)
        await session.commit()

        return {"status": "ok"}
