from pydantic import BaseModel, ConfigDict, Field


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    desription: str
    price: int
    quanity: int


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomPATCH(BaseModel):
    hotel_id: int | None = Field(None)
    title: str | None = Field(None)
    desription: str | None = Field(None)
    price: int | None = Field(None)
    quanity: int | None = Field(None)
