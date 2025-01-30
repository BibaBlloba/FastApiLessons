from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, Body, HTTPException, Response
from passlib.context import CryptContext

from repos.users import UsersRepository
from schemas.users import UserAdd, UserLogin, UserRequestAdd
from src.database import async_session_maker

"""Переменные окружения"""
SECRET_KEY = "some_random_letters"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXIPRE_MINUTES = 30


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXIPRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


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


@router.post("/login")
async def login_user(
    data: UserLogin,
    response: Response,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_uesr_with_hashedPwd(email=data.email)
        if not user:
            raise HTTPException(
                status_code=401, detail="Пользователь с таким email не зарегестрирован."
            )
        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")
        access_token = create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}
