from django import template
from django.shortcuts import get_object_or_404
from cart.models import OrderItem
from mainapp.models import Product
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter
def cart_qty(user):
    if user.is_authenticated:
        qs = OrderItem.objects.filter(user__username=user)
        if qs.exists():
            return qs.count()
    return 0

