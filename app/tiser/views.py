import logging

from accounts.models import TiserUser
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Category, Tiser, TiserStatus
from .serializers import (CategorySerializer, TiserListPaymentSerializer,
                          TiserListSerializer, TiserPaymentResponseSerializer,
                          TiserSerializer)

logger = logging.getLogger(__name__)


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


class TiserList(generics.ListCreateAPIView):
    serializer_class = TiserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category", "status"]

    def get_queryset(self):
        objects = Tiser.objects.all().order_by("created_at")
        if self.request.user.is_staff:
            return objects
        return objects.filter(author=self.request.user.id)


class TiserPayment(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = TiserListPaymentSerializer

    @staticmethod
    def save_payment(payed_tisers: list, tiser_price: float):
        tisers = Tiser.objects.filter(
            id__in=payed_tisers,
            status=TiserStatus.CREATED
        )
        logger.debug("Payment for tisers requested: %s", tisers)

        payment_count = 0
        with transaction.atomic():
            for tiser in tisers:
                # set tisers PAYED status
                payment_count += Tiser.objects.select_for_update().filter(id=tiser.id).update(
                    status=TiserStatus.PAYED,
                    price=tiser_price,
                    updated_at=timezone.now()
                )
                # increase author's amount
                TiserUser.objects.select_for_update().filter(id=tiser.author.id).update(
                    amount=F("amount") + tiser_price
                )
                logger.info("Tiser payment accepted: %s", tiser)

        return payment_count

    @swagger_auto_schema(
        operation_id="Apply tisers payment",
        operation_summary="Apply tisers payment",
        operation_description="Apply tisers payment with the given price.",
        tags=["payment"],
        request_body=TiserListPaymentSerializer,
        responses={200: TiserPaymentResponseSerializer()}
    )
    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payed_tisers = serializer.data.get("tisers", [])
        tiser_price = int(serializer.data.get("price"))
        payment_count = self.save_payment(payed_tisers, tiser_price)

        return Response(
            {"message": "Payment accepted", "count": payment_count},
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_id="Cancel tisers payment",
        operation_summary="Cancel tisers payment",
        operation_description="Set tisers statuses to cancelled.",
        tags=["payment"],
        request_body=TiserListSerializer,
        responses={200: TiserPaymentResponseSerializer()}
    )
    def patch(self, request, *args, **kwargs):
        serializer = TiserListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tisers = serializer.data.get("tisers", [])

        with transaction.atomic():
            cancel_count = Tiser.objects.select_for_update().filter(
                id__in=tisers,
                status=TiserStatus.CREATED
            ).update(
                status=TiserStatus.CANCELLED,
                updated_at=timezone.now()
            )
        logger.info("Tisers payment cancelled: %s", tisers)

        return Response(
            {"message": "Tisers payment cancelled", "count": cancel_count},
            status=status.HTTP_200_OK
        )
