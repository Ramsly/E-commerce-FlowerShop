from django import template
from mainapp.models import Order

register = template.Library()

@register.filter
def wishlist_qty(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user)
        if qs.exists():
            return qs[0].count()
    return 0