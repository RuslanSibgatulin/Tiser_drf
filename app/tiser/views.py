from datetime import datetime

from accounts.models import TiserUser
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Category, Tiser, TiserStatus
from .serializers import (CategorySerializer, TiserListPaymentSerializer,
                          TiserListSerializer, TiserPaymentResponseSerializer,
                          TiserSerializer)


class TiserList(generics.ListCreateAPIView):
    serializer_class = TiserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category", "status"]

    def get_queryset(self):
        objects = Tiser.objects.all().order_by("created_at")
        if self.request.user.is_staff:
            return objects
        return objects.filter(author=self.request.user.id)


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all().order_by("title")
    serializer_class = CategorySerializer


class CategoryCreate(generics.CreateAPIView):
    queryset = Category.objects.all().order_by("title")
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all().order_by("title")
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ["put", "delete"]


class TiserPayment(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = TiserListPaymentSerializer

    @swagger_auto_schema(
        operation_description="Apply tisers payment with price",
        request_body=TiserListPaymentSerializer,
        responses={200: TiserPaymentResponseSerializer()}
    )
    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payed_tisers = serializer.data.get("tisers", [])
        tiser_price = serializer.data.get("price")

        tisers = Tiser.objects.filter(
            id__in=payed_tisers,
            status=TiserStatus.CREATED
        )
        payment_count = tisers.update(
            status=TiserStatus.PAYED,
            price=tiser_price,
            updated_at=datetime.now()
        )

        # TODO: increase authors amount
        Counter.objects.filter(name=name).update(count=F("count") + 1)

        return Response(
            {"message": "Payment accepted", "count": payment_count},
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_description="Cancel tisers without payment",
        request_body=TiserListSerializer,
        responses={200: TiserPaymentResponseSerializer()}
    )
    def patch(self, request, *args, **kwargs):
        serializer = TiserListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tisers = serializer.data.get("tisers", [])

        cancel_count = Tiser.objects.filter(
            id__in=tisers,
            status=TiserStatus.CREATED
        ).update(
            status=TiserStatus.CANCELLED,
            updated_at=datetime.now()
        )

        return Response(
            {"message": "Tisers cancelled for payment", "count": cancel_count},
            status=status.HTTP_200_OK
        )
