async def test_get_hotels(ac):
    hotels = await ac.get(
        url='/hotels',
        params={
            'date_from': '2025-01-01',
            'date_to': '2026-01-01',
        },
    )
    assert hotels.status_code == 200
