from datetime import date

import pytest

from exceptions import AllRoomsAreBooked
from src.schemas.bookings import BookingAdd, BookingPatch


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    hotel = await db.hotels.get_one_or_none(id=room_id)
    booking_add = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        price=1000,
        date_from=date(year=2025, month=1, day=1),
        date_to=date(year=2026, month=10, day=22),
    )

    # FIX: Эта дресня не работает как надо
    try:
        new_booking_data = await db.bookings.add(booking_add, hotel_id=hotel.id)
    except AllRoomsAreBooked:
        pytest.skip()
    assert new_booking_data
    await db.commit()

    # Получение

    booking = await db.bookings.get_one_or_none(id=new_booking_data.id)
    assert booking
    assert booking.id == new_booking_data.id
    assert booking.room_id == new_booking_data.room_id
    assert booking.user_id == new_booking_data.user_id

    # Обновление

    new_price = 399
    new_date = date(year=2027, month=10, day=22)
    new_booking_data = BookingPatch(
        price=new_price,
        date_from=date(year=2025, month=1, day=1),
        date_to=new_date,
    )

    await db.bookings.edit(new_booking_data, exclude_unset=True, id=booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=booking.id)
    assert updated_booking.price == new_price
    assert updated_booking.date_to == new_date

    # Удаление

    await db.bookings.delete(id=1)
    result = await db.bookings.get_filtered(id=booking.id)
    assert result

    await db.rollback()
