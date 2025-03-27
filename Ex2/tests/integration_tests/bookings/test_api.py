async def test_add_booking(db, authenticated_ac):
    room_id = (await db.rooms.get_all())[0].id

    for i in range(3):
        response = await authenticated_ac.post(
            "/bookings",
            json={
                "room_id": room_id,
                "date_from": "2025-01-01",
                "date_to": "2026-07-08",
            },
        )

        if i == 2:
            assert response.status_code == 404
        else:
            assert response.status_code == 200
