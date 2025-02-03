from pydantic import BaseModel, EmailStr, Field


class UserPatch(BaseModel):
    nickname: str | None = Field(None)
    email: str | None = Field(None)
    password: str | None = Field(None)


class UserRequestAdd(BaseModel):
    nickname: str
    password: str
    email: EmailStr | None = Field(None)


class UserAdd(BaseModel):
    nickname: str
    hashed_password: str
    email: EmailStr | None = Field(None)


class User(UserAdd):
    id: int
