from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRequestAdd(BaseModel):
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    login: str

    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserAdd(BaseModel):
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    login: str

    email: EmailStr
    hashed_password: str


class User(BaseModel):
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    login: str | None = Field(None)

    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserHashedPwd(User):
    hashed_password: str
