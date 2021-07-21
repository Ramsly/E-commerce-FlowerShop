from django.urls import path
from .views import *

app_name = "cart"

urlpatterns = [
    path("", cart, name='cart'),
    path("add/", cart_add, name='cart-add'),
    path("remove/", cart_delete_item, name='cart-remove'),
    path("delete/", cart_delete_all, name='cart-delete-all'),
]
