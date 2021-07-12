from django.urls import path
from .views import *

app_name = "wishlist"

urlpatterns = [
    path("", wishes, name='wishlist'),
    path("<id>/add/", wishes_add, name='wishlist-add'),
    path("<id>/remove/", wishes_delete_item, name='wishlist-remove'),
    path("delete/", wishes_delete_all, name='wishlist-delete-all'),
]
