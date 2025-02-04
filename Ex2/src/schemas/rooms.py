from pydantic import BaseModel, ConfigDict, Field


class RoomAddRequest(BaseModel):
    title: str
    desription: str | None = Field(None)
    price: int
    quanity: int


class RoomAdd(RoomAddRequest):
    hotel_id: int


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomPatchRequest(BaseModel):
    title: str | None = Field(None)
    desription: str | None = Field(None)
    price: int | None = Field(None)
    quanity: int | None = Field(None)


class RoomPatch(RoomPatchRequest):
    hotel_id: int | None = Field(None)
