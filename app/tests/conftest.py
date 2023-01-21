from http import HTTPStatus

import pytest
from rest_framework.test import APIClient

API_URL = "http://127.0.0.1:8000/api/v1/"
AUTHOR_NAME = "author1"
MANAGER_NAME = "manager1"


@pytest.fixture
def api_url():
    return API_URL


@pytest.fixture
def user_author(django_user_model):
    return django_user_model.objects.create_user(username=AUTHOR_NAME, password=AUTHOR_NAME, is_staff=False)


@pytest.fixture
def user_manager(django_user_model):
    return django_user_model.objects.create_user(username=MANAGER_NAME, password=MANAGER_NAME, is_staff=True)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def client_is_author(api_client, api_url, user_author):
    data = {
        "username": AUTHOR_NAME,
        "password": AUTHOR_NAME
    }
    response = api_client.post(api_url + "token-auth/", data=data)
    user_token = response.json()["token"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {user_token}")
    return api_client


@pytest.fixture
def category():
    from tiser.models import Category
    return Category.objects.create(title="Category 1")


@pytest.fixture
def tiser(user_author, category):
    from tiser.models import Tiser
    return Tiser.objects.create(title="Tiser 1", author=user_author, category=category)
