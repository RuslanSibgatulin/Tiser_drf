from http import HTTPStatus

import pytest
from rest_framework.test import APIClient


@pytest.mark.parametrize(
    "url",
    ["categories/", "tisers/"]
)
def test_get_anon(api_client: APIClient, api_url: str, url: str):
    url = api_url + url
    response = api_client.get(url)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.parametrize(
    "url,data",
    [
        ("categories/add", {"title": "title"}),
        ("tisers/", {"category": 1, "title": "title"})
    ]
)
def test_post_anon(api_client: APIClient, api_url: str, url: str, data: dict):
    url = api_url + url
    response = api_client.post(url, data=data)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
