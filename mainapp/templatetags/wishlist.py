from django import template
from wishlist.models import OrderItem

register = template.Library()

@register.filter
def wishlist_qty(user):
    if user.is_authenticated:
        qs = OrderItem.objects.filter(user__username=user)
        if qs.exists():
            return qs.count()
    return 0
