from decimal import Decimal

from cart.models import OrderItem
from mainapp.models import Product
from django.db.models.aggregates import Sum



def cart_session(request):
    return {"cart_session": request.session.get("cart")}


def total_price(request):
    try:
        total_pr = sum(
            Decimal(item["price"]) * item["qty"] for item in request.session.get("cart")
        )
    except TypeError:
        total_pr = 0
    return {"total_price": total_pr}


def total_qty_cart(request):
    try:
        total_qty = sum(item["qty"] for item in request.session.get("cart"))
    except TypeError:
        total_qty = 0
    return {"total_qty_cart": total_qty}


def order_items_cart(request):
    return {"order_items_cart": OrderItem.objects.filter(user__username=request.user)}


def get_cart_qty_auth(request):
    get_cart_qty_auth = (
        OrderItem.objects.filter(user__username=request.user)
        .aggregate(get_cart_qty_auth=Sum("quantity"))
        .get("get_cart_qty_auth")
    )
    if get_cart_qty_auth is None:
        return {"get_cart_qty_auth": 0}
    return {"get_cart_qty_auth": get_cart_qty_auth}


def get_cart_total_auth(request):
    get_cart_total_auth = (
        OrderItem.objects.filter(user__username=request.user)
        .aggregate(get_cart_total_auth=Sum("product__price") * Sum("quantity"))
        .get("get_cart_total_auth")
    )
    if get_cart_total_auth is None:
        return {"get_cart_total_auth": 0}
    return {"get_cart_total_auth": get_cart_total_auth}
