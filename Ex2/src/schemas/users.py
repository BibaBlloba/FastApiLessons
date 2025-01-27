from pydantic import BaseModel, ConfigDict, Field


class UserRequestAdd(BaseModel):
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    login: str | None = Field(None)

    email: str
    password: str


class UserAdd(BaseModel):
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    login: str | None = Field(None)

    email: str
    hashed_password: str


class User(BaseModel):
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    login: str | None = Field(None)

    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)
