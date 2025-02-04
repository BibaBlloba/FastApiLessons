from fastapi import APIRouter

from schemas.bookings import BookingAdd

router = APIRouter(prefix="/bookings", tags=["Брони"])


@router.post("/test")
async def test(
    data: BookingAdd,
):
    return {"test": data}
