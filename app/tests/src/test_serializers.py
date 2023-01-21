from tiser.serializers import (CategorySerializer, TiserListPaymentSerializer,
                               TiserListSerializer,
                               TiserPaymentResponseSerializer, TiserSerializer)


def test_CategorySerializer():
    serializer = CategorySerializer()
    assert list(serializer.get_fields()) == ["id", "title"]


def test_TiserListPaymentSerializer():
    serializer = TiserListPaymentSerializer()
    assert list(serializer.get_fields()) == ["tisers", "price"]


def test_TiserListSerializer():
    serializer = TiserListSerializer()
    assert list(serializer.get_fields()) == ["tisers"]


def test_TiserPaymentResponseSerializer():
    serializer = TiserPaymentResponseSerializer()
    assert list(serializer.get_fields()) == ["message", "count"]


def test_TiserSerializer():
    serializer = TiserSerializer()
    assert list(serializer.get_fields()) == [
        "id", "author", "category", "title", "desc", "status", "price", "created_at", "updated_at"
    ]
