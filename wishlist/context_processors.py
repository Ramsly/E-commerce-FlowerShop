from django.shortcuts import get_object_or_404


def wishes_session(request):
    return {"wishes_session": request.session.get("wishlist")}

def total_qty_wishlist(request):
    try:
        total_qty = sum(item["qty"] for item in request.session.get("wishlist"))
    except TypeError:
        total_qty = 0
    return {"total_qty_wishlist": total_qty}