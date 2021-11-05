from wishlist.models import OrderItem


def wishes_session(request):
    return {"wishes_session": request.session.get("wishlist")}

def total_qty_wishlist(request):
    try:
        total_qty = sum(item["qty"] for item in request.session.get("wishlist"))
    except TypeError:
        total_qty = 0
    return {"total_qty_wishlist": total_qty}

def wishlist_items(request):
    return {"wishlist_items": OrderItem.objects.filter(user__username=request.user)}