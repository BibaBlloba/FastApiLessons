from fastapi import APIRouter, Body, HTTPException

from api.dependencies import DbDep, UserIdDap
from exceptions import AllRoomsAreBooked
from schemas.bookings import BookingAdd, BookingAddRequest
from services.bookings import BookingsService

router = APIRouter(prefix='/bookings', tags=['Брони'])


@router.get('')
async def get_all(
    db: DbDep,
):
    return await db.bookings.get_all()


@router.get('/me')
async def get_my_bookings(
    db: DbDep,
    user_id: UserIdDap,
):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post('')
async def test(
    db: DbDep,
    user_id: UserIdDap,
    data: BookingAddRequest = Body(
        openapi_examples={
            '1': {
                'summary': 'first bookign',
                'value': {
                    'room_id': 1,
                    'date_from': '2025-02-10',
                    'date_to': '2025-02-15',
                },
            }
        }
    ),
):
    try:
        await BookingsService(db).create_facility(data, user_id)
    except AllRoomsAreBooked as ex:
        raise HTTPException(409, detail=ex.detail)
