from pydantic import BaseModel, ConfigDict, Field

from src.schemas.facilities import Facility


class RoomAddRequest(BaseModel):
    title: str
    desription: str | None = Field(None)
    price: int
    quantity: int = 1
    facilities_ids: list[int] = []


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    desription: str | None = Field(None)
    price: int
    quantity: int


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomWithRels(Room):
    facilities: list[Facility]


class RoomPatchRequest(BaseModel):
    title: str | None = Field(None)
    desription: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
    facilities_ids: list[int] | None = []


class RoomPatch(BaseModel):
    hotel_id: int | None = Field(None)
    title: str | None = Field(None)
    desription: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
