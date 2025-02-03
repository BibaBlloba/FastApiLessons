from fastapi import APIRouter, HTTPException, Request, Response

from database import async_session_maker
from repos.users import UsersRepository
from schemas.user import UserAdd, UserRequestAdd
from services.auth import AuthService

router = APIRouter(prefix="", tags=["Auth"])


@router.get("/me")
async def get_me():
    return {"status": "keka"}


@router.post("/register")
async def register_user(
    user_data: UserRequestAdd,
):
    hashed_password = AuthService().hash_password(user_data.password)
    hashed_user_data = UserAdd(
        nickname=user_data.nickname,
        hashed_password=hashed_password,
        email=user_data.email,
    )
    async with async_session_maker() as session:
        try:
            result = await UsersRepository(session).add(hashed_user_data)
        except:
            raise HTTPException(status_code=409, detail="User alredy registered")
        await session.commit()
        return {"status": "ok"}


@router.post("/login")
async def login(
    user_data: UserRequestAdd,
    response: Response,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashedPwd(
            user_data.nickname
        )
        if not user:
            raise HTTPException(status_code=401, detail="Incorrect login credentials")
        if not AuthService().verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect login credentials")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.get("/secret_data")
async def get_sercet_data(
    request: Request,
):
    access_token = request.cookies.get("access_token", None)
    if access_token is None:
        raise HTTPException(status_code=401)
    return {"sercet": "Super Secret Data"}
