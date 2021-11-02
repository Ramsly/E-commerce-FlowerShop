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

@register.filter
def get_product_id_in_cart(id):
    product = get_object_or_404(Product, id=id)
    if product.exists():
        return product[0]
    return None
    

