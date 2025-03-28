import pytest


@pytest.fixture()
async def prune_bookings(db):
    await db.bookings.delete()
    await db.commit()


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
    "room_id, date_from, date_to, status_code",
    [
        (1, "2025-01-01", "2025-01-01", 200),
        (1, "2025-01-01", "2025-01-01", 200),
    ],
)
async def test_get_booking(
    prune_bookings, authenticated_ac, db, room_id, date_from, date_to, status_code
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    request = await authenticated_ac.get("/bookings")
    request_json = request.json()
    print(request_json)
    assert request.status_code == status_code
    assert request_json[0]["room_id"] == room_id
