from django.urls import path
from .views import *

app_name = "cart"

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path(
        "<int:id>/add-authenticated/",
        AddProductToCartAuthenticatedUserView.as_view(),
        name="cart-add-authenticated",
    ),
    path(
        "<int:id>/add-not-authenticated/",
        AddProductToCartNotAuthenticatedUserView.as_view(),
        name="cart-add-not-authenticated",
    ),
    path(
        "<int:id>/remove-authenticated/",
        DeleteProductFromCartAuthenticatedUserView.as_view(),
        name="cart-remove-authenticated",
    ),
    path(
        "<int:id>/remove-not-authenticated/",
        DeleteProductFromCartNotAuthenticatedUserView.as_view(),
        name="cart-remove-not-authenticated",
    ),
    path(
        "delete-authenticatedkd/",
        DeleteAllProductsFromCartAuthenticatedUserView.as_view(),
        name="cart-delete-all-authenticated",
    ),
    path(
        "delete-not-authenticated/",
        DeleteAllProductsFromCartAuthenticatedUserView.as_view(),
        name="cart-delete-all-not-authenticated",
    ),
]
