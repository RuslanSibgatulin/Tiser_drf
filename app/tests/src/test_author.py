from http import HTTPStatus

from rest_framework.test import APIClient
from tiser.models import Category, Tiser, TiserStatus


def test_get_categories(client_is_author: APIClient, api_url: str):
    url = api_url + "categories/"
    response = client_is_author.get(url)
    assert response.status_code == HTTPStatus.OK


def test_deny_add_category(client_is_author: APIClient, api_url: str):
    url = api_url + "categories/add"
    data = {
        "title": "foo"
    }
    response = client_is_author.post(url, data=data)
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_deny_put_category(client_is_author: APIClient, api_url: str, category: Category):
    url = f"{api_url}categories/{category.id}/"
    data = {
        "title": "foo"
    }
    response = client_is_author.put(url, data=data)
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_deny_delete_category(client_is_author: APIClient, api_url: str, category: Category):
    url = f"{api_url}categories/{category.id}/"
    response = client_is_author.delete(url)
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_get_tisers(client_is_author: APIClient, api_url: str, tiser: Tiser):
    url = api_url + "tisers/"
    response = client_is_author.get(url)
    assert response.status_code == HTTPStatus.OK
    assert response.json()["count"] == 1
    tiser = response.json()["results"][0]
    assert tiser["status"] == TiserStatus.CREATED


def test_post_tiser(client_is_author: APIClient, api_url: str, category: Category):
    url = api_url + "tisers/"
    data = {
        "category": category.id,
        "title": "tiser 1",
        "desc": "tiser description"
    }
    response = client_is_author.post(url, data=data)
    assert response.status_code == HTTPStatus.CREATED
    tiser = response.json()
    assert tiser["title"] == data["title"]
    assert tiser["status"] == TiserStatus.CREATED
