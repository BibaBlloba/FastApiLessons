async def test_get_facilities(ac):
    facilities = await ac.get(
        url="/facilities",
    )
    assert facilities.status_code == 200
    assert isinstance(facilities.json(), list)


async def test_post_facilities(ac):
    response = await ac.post(url="/facilities", json={"title": "test_facility"})
    print(response.json())
    assert response.status_code == 201
