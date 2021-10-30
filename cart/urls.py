from django.urls import path
from .views import *

app_name = "cart"

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("<int:id>/add/", AddProductToCartView.as_view(), name="cart-add"),
    path("<int:id>/remove/", DeleteProductFromCartView.as_view(), name="cart-remove"),
    path("delete/", DeleteAllProductsFromCartView.as_view(), name="cart-delete-all"),
]
