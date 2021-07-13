from django.shortcuts import redirect, render
from mainapp.models import Product
from django.http import JsonResponse
from .utils import *
# from django.views.decorators.csrf import csrf_exempt


def cart(request):
    context = {
        "cart_session": request.session.get("cart"),
    }
    return render(request, "cart.html", context)


def cart_add(request, id):
    if request.method == "POST":
        if not request.session.get("cart"):
            request.session["cart"] = list()
        else:
            request.session["cart"] = list(request.session["cart"])
        item_exist = next(
            (item for item in request.session["cart"] if item["id"] == int(id)),
            False,
        )
        price = float(replace_to_dot(request.POST.get("price")))
        add_data = {
            "id": int(id),
            "title": request.POST.get("title"),
            "qty": 1,  # request.POST.get("получить из input в форме")
            "price": price,
            "total_price_cart": price * 1
        }
        if not item_exist:
            request.session["cart"].append(add_data)
            if request.session.get('wishlist'):
                for item in request.session["wishlist"]:
                    if item["id"] == int(id):
                        item.clear()

                    while {} in request.session["wishlist"]:
                        request.session["wishlist"].remove({})

                    if not request.session["wishlist"]:
                        del request.session["wishlist"]
            request.session.modified = True
    return redirect(request.POST.get("url_from"))


def cart_delete_item(request, id):
    if request.method == "POST":
        for item in request.session["cart"]:
            if item["id"] == int(id):
                item.clear()

        while {} in request.session["cart"]:
            request.session["cart"].remove({})

        if not request.session["cart"]:
            del request.session["cart"]

        request.session.modified = True

    return redirect(request.POST.get("url_from"))


def cart_delete_all(request):
    if request.session.get("cart"):
        del request.session["cart"]
    return redirect(request.POST.get("url_from"))
