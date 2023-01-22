from http import HTTPStatus

from rest_framework.test import APIClient
from tiser.models import Category, Tiser, TiserStatus


def test_get_categories(client_is_manager: APIClient, api_url: str):
    url = api_url + "categories/"
    response = client_is_manager.get(url)
    assert response.status_code == HTTPStatus.OK


def test_add_category(client_is_manager: APIClient, api_url: str):
    url = api_url + "categories/add"
    data = {
        "title": "foo"
    }
    response = client_is_manager.post(url, data=data)
    assert response.status_code == HTTPStatus.CREATED


def test_put_category(client_is_manager: APIClient, api_url: str, category: Category):
    url = f"{api_url}categories/{category.id}/"
    data = {
        "title": "bar"
    }
    response = client_is_manager.put(url, data=data)
    assert response.status_code == HTTPStatus.OK


def test_delete_category(client_is_manager: APIClient, api_url: str, category: Category):
    url = f"{api_url}categories/{category.id}/"
    response = client_is_manager.delete(url)
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_get_tisers(client_is_manager: APIClient, api_url: str, tiser: Tiser):
    url = api_url + "tisers/"
    response = client_is_manager.get(url)
    assert response.status_code == HTTPStatus.OK
    assert response.json()["count"] == 1
    tiser = response.json()["results"][0]
    assert tiser["status"] == TiserStatus.CREATED


def test_agree_tiser_payment(client_is_manager: APIClient, api_url: str, tiser: Tiser):
    url = api_url + "tisers/payment"
    data = {
        "tisers": [tiser.id],
        "price": 50
    }
    author_amount_before = tiser.author.amount
    response = client_is_manager.put(url, data=data)
    assert response.status_code == HTTPStatus.OK
    assert response.json()["count"] == 1

    tiser.refresh_from_db()
    assert tiser.author.amount == author_amount_before + data["price"]
    assert tiser.price == data["price"]
    assert tiser.status == TiserStatus.PAYED


def test_deny_tiser_payment(client_is_manager: APIClient, api_url: str, tiser: Tiser):
    url = api_url + "tisers/payment"
    data = {
        "tisers": [tiser.id],
    }

    response = client_is_manager.patch(url, data=data)
    assert response.status_code == HTTPStatus.OK
    assert response.json()["count"] == 1

    tiser.refresh_from_db()
    assert tiser.status == TiserStatus.CANCELLED
