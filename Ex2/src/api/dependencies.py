from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Query, Request
from pydantic import BaseModel

from database import async_session_maker
from services.auth import AuthService
from utils.db_manager import DbManager


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, ge=1)]
    per_page: Annotated[int | None, Query(default=None, ge=1, le=10)]


PaginationDap = Annotated[PaginationParams, Depends()]


def get_token(
    request: Request,
) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Вы не предоставили токен доступа.")
    return token


def get_current_user_id(token: str = Depends(get_token)):
    try:
        data = AuthService().decode_token(token)
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Токен не действителен.")
    return data.get("user_id")


UserIdDap = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DbManager(session_factory=async_session_maker) as db:
        yield db


DbDep = Annotated[DbManager, Depends(get_db)]
