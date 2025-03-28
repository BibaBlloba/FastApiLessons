import pytest


@pytest.mark.parametrize(
    "email, password, first_name, last_name, login, registered_status_code",
    [
        ("example@user2.com", "123", "Keka", "Xui", "kekel2", 200),
        ("example@user2.com", "123", "Keka", "Xui", "kekel2", 401),
        ("example@user3.com", "123", "Keka", "Xui", "kekel3", 200),
        ("example@user4.com", "123", "Keka", "Xui", "kekel4", 200),
        ("example@user5.com", "", "Keka", "Xui", "kekel6", 401),
        ("example@user6.com", "123", "Keka", "Xui", "", 401),
        ("asd", "", "Keka", "Xui", "", 422),
    ],
)
async def test_register(
    email,
    password,
    first_name,
    last_name,
    login,
    authenticated_ac,
    registered_status_code,
):
    response_register = await authenticated_ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "login": login,
        },
    )
    print(response_register.json())
    assert response_register.status_code == registered_status_code
    if response_register.status_code != 200:
        # pytest.skip() # Так делать не надо!
        return

    response_login = await authenticated_ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    response_me = await authenticated_ac.get("/auth/me")
    assert response_me.status_code == 200
    assert response_me.json()["login"] == login

    print(response_login.json())
    assert response_login.status_code == 200
    assert type(response_login.json()["access_token"]) == str

    response_logout = await authenticated_ac.post("/auth/logout")
    response_me = await authenticated_ac.get("/auth/me")
    assert response_me.status_code == 401
