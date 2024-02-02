import pytest
"""Тесты регистрация+логин"""


@pytest.mark.django_db
def test_user_registration_and_token_authentication(client):
    registration_url = '/api/users/'
    registration_data = {
        "email": "test@example.com",
        "username": "testuser",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "password": "testpassword"
    }

    registration_response = client.post(
        registration_url, data=registration_data)

    assert registration_response.status_code == 201
    assert registration_response.json()["email"] == "test@example.com"

    from users.models import User
    user = User.objects.get(username="testuser")
    assert user.first_name == "Вася"
    assert user.last_name == "Пупкин"

    authentication_url = '/api/auth/token/login/'
    authentication_data = {
        "email": "test@example.com",
        "password": "testpassword"
    }

    authentication_response = client.post(
        authentication_url, data=authentication_data)

    assert authentication_response.status_code == 200
    assert "auth_token" in authentication_response.json()
