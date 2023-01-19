from django.test import TestCase
from tiser.serializers import (CategorySerializer, TiserListPaymentSerializer,
                               TiserListSerializer,
                               TiserPaymentResponseSerializer, TiserSerializer)


class SerializersTestClass(TestCase):

    def test_CategorySerializer(self):
        serializer = CategorySerializer()
        self.assertEqual(
            list(serializer.get_fields()), ["id", "title"]
        )

    def test_TiserListPaymentSerializer(self):
        serializer = TiserListPaymentSerializer()
        self.assertEqual(
            list(serializer.get_fields()), ["tisers", "price"]
        )

    def test_TiserListSerializer(self):
        serializer = TiserListSerializer()
        self.assertEqual(
            list(serializer.get_fields()), ["tisers"]
        )

    def test_TiserPaymentResponseSerializer(self):
        serializer = TiserPaymentResponseSerializer()
        self.assertEqual(
            list(serializer.get_fields()), ["message", "count"]
        )

    def test_TiserSerializer(self):
        serializer = TiserSerializer()
        self.assertEqual(
            list(serializer.get_fields()),
            ["id", "author", "category", "title", "desc", "status", "price", "created_at", "updated_at"]
        )
