from decimal import Decimal

def cart_session(request):
    return {"cart_session": request.session.get("cart")}

def total_price(request):
    try:
        total_pr = sum(Decimal(item['price']) * item['qty'] for item in request.session.get("cart"))
    except TypeError:
        total_pr = 0
    return {"total_price": total_pr}

def total_qty_cart(request):
    try:
        total_qty = sum(item["qty"] for item in request.session.get("cart"))
    except TypeError:
        total_qty = 0
    return {"total_qty_cart": total_qty}