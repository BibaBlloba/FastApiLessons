import pytest


@pytest.mark.parametrize(
    'hotel_id, status_code',
    [(1, 200), (2, 200)],
)
async def test_get_rooms(ac, hotel_id, status_code):
    rooms = await ac.get(
        url=f'/hotels/{hotel_id}/rooms',
        params={
            'date_from': '2025-01-01',
            'date_to': '2026-01-01',
        },
    )
    print(rooms.json())
    assert rooms.status_code == 200


@pytest.mark.parametrize(
    'hotel_id, status_code',
    [(1, 200)],
)
async def test_add_rooms(ac, hotel_id, status_code):
    room = await ac.post(
        f'/hotels/{hotel_id}/rooms',
        json={
            'title': 'Test Room',
            'desription': 'string',
            'price': 69000,
            'quantity': 69,
            'facilities_ids': [],
        },
    )
    print(room.json())
    assert room.status_code == status_code


@pytest.mark.parametrize(
    'hotel_id, room_id, status_code, title',
    [
        (1, 5, 200, 'Test Room'),
        (2, 10, 404, ''),
        (30, 10, 404, ''),
    ],
)
async def test_get_test_room(ac, hotel_id, room_id, status_code, title):
    result = await ac.get(
        url=f'/hotels/{hotel_id}/rooms/{room_id}',
    )
    room = result.json()
    print(room)
    assert result.status_code == status_code
    if result.status_code == 404:
        return
    assert room['title'] == title
