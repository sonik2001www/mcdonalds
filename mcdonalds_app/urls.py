from django.urls import path
from .views import ProductList, ProductDetail, ProductFieldDetail

urlpatterns = [
    path("all_products/", ProductList.as_view(), name="all_products"),
    path(
        "products/<str:product_name>/",
        ProductDetail.as_view(),
        name="product_detail"
    ),
    path(
        "products/<str:product_name>/<str:product_field>/",
        ProductFieldDetail.as_view(),
        name="product_field_detail"
    ),
]

app_name = "mcdonalds_app"
