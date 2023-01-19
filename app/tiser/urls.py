from django.urls import path

from .views import (CategoryCreate, CategoryDetail, CategoryList, TiserList,
                    TiserPayment)

app_name = "tiser_api"

urlpatterns = [
    path("tisers/", TiserList.as_view()),
    path("tisers/payment", TiserPayment.as_view()),
    path("categories/", CategoryList.as_view()),
    path("categories/add", CategoryCreate.as_view()),
    path("categories/<int:pk>/", CategoryDetail.as_view()),
]
