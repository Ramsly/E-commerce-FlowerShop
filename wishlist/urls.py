from django.urls import path
from .views import *

app_name = "wishlist"

urlpatterns = [
    path("", WishesView.as_view(), name='wishlist'),
    path("<int:id>/add/", AddProductToWishesView.as_view(), name='wishlist-add'),
    path("<int:id>/remove/", DeleteProductFromWishesView.as_view(), name='wishlist-remove'),
    path("delete/", DeleteAllProductsFromWishesView.as_view(), name='wishlist-delete-all'),
]
