from datetime import date

from pydantic import BaseModel, ConfigDict


class BookingAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingAdd(BookingAddRequest):
    user_id: int
    price: int


class Booking(BookingAdd):
    id: int
    created_at: date

    model_config = ConfigDict(from_attributes=True)


class BookingPatch(BaseModel):
    user_id: int | None = None
    price: int | None = None
    room_id: int | None = None
    date_from: date | None = None
    date_to: date | None = None
