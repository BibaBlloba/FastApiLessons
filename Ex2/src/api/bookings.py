from fastapi import APIRouter, Body

from api.dependencies import DbDep, UserIdDap
from schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(prefix="/bookings", tags=["Брони"])


@router.post("/")
async def test(
    db: DbDep,
    user_id: UserIdDap,
    data: BookingAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "first bookign",
                "value": {
                    "room_id": 1,
                    "date_from": "2025-02-10",
                    "date_to": "2025-02-15",
                },
            }
        }
    ),
):
    room = await db.rooms.get_one_or_none(id=data.room_id)
    room_price: int = room.price
    _data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **data.dict(),
    )
    result = await db.bookings.add(_data)
    await db.commit()
    return result


@router.get("/")
async def get_all(
    db: DbDep,
):
    return await db.bookings.get_all()
