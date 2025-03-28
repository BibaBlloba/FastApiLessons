# ruff: noqa: F841
import pytest

from tests.conftest import get_db_null_pull


@pytest.fixture(scope="module")
async def prune_bookings():
    async for _db in get_db_null_pull():
        await _db.bookings.delete()
        await _db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2025-01-01", "2025-01-01", 200),
        (1, "2025-01-01", "2025-01-01", 200),
        (1, "2025-01-01", "2025-01-01", 400),
    ],
)
async def test_add_booking(
    db, authenticated_ac, room_id, date_from, date_to, status_code
):
    room_id = (await db.rooms.get_all())[0].id

    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "room_id, date_from, date_to, booked_rooms",
    [
        (1, "2025-01-01", "2025-01-01", 1),
        (1, "2025-01-01", "2025-01-01", 2),
    ],
)
async def test_get_booking(
    room_id,
    date_from,
    date_to,
    booked_rooms,
    prune_bookings,
    db,
    authenticated_ac,
):
    response = await authenticated_ac.post(  # noqa
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    my_books = await authenticated_ac.get("/bookings/me")
    my_books_json = my_books.json()
    print(my_books_json)
    assert len(my_books.json()) == booked_rooms
    assert my_books.status_code == 200
    assert my_books_json[0]["room_id"] == room_id
