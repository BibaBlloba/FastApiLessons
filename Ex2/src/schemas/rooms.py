from pydantic import BaseModel, ConfigDict, Field


class RoomAddRequest(BaseModel):
    title: str
    desription: str | None = Field(None)
    price: int
    quanity: int = 1
    facilities_ids: list[int] = []


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    desription: str | None = Field(None)
    price: int
    quanity: int


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomPatchRequest(BaseModel):
    title: str | None = Field(None)
    desription: str | None = Field(None)
    price: int | None = Field(None)
    quanity: int | None = Field(None)
    facilities_ids: list[int] | None = None


class RoomPatch(BaseModel):
    hotel_id: int | None = Field(None)
    title: str | None = Field(None)
    desription: str | None = Field(None)
    price: int | None = Field(None)
    quanity: int | None = Field(None)
