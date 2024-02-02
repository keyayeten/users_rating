import pytest
from users.models import User
from rest_framework.test import APIClient


@pytest.fixture
def user():
    return User.objects.create(
        username='testuser',
        email='test@example.com')


@pytest.fixture
def client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def user_data():
    data = {'email': 'test@example.com',
            'id': 1,
            'username': 'testuser',
            'first_name': '',
            'last_name': ''}
    return data


@pytest.mark.django_db
def test_create_post(client, user_data):
    url = '/api/posts/'
    data = {
        "author": 1,
        "text": "test_text_test"
    }

    response = client.post(url, data=data)

    assert response.status_code == 201
    assert response.json()["author"] == user_data
    assert response.json()["text"] == "test_text_test"
