from django import template
from cart.models import OrderItem
from mainapp.models import Product
from django.db.models import Sum, Count

register = template.Library()


@register.filter
def cart_qty(user):
    if user.is_authenticated:
        qs = OrderItem.objects.filter(user__username=user).aggregate(total_qty=Count("quantity")).get("total_qty")
        return qs
    return 0

# @register.filter
# def cart_total_price(user):
#     if user.is_authenticated:
#         qs = OrderItem.objects.filter(user__username=user).aggregate(total_sum=Sum("product__price")).get('total_sum')
#         return qs
#     return 0
