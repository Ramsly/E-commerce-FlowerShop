from django.http import JsonResponse
from django.shortcuts import redirect, render

from .utils import *


def cart(request):
    context = {
        "cart_session": request.session.get("cart"),
    }
    return render(request, "cart.html", context)


def cart_add(request):
    if request.is_ajax():
        if not request.session.get("cart"):
            request.session["cart"] = list()
        else:
            request.session["cart"] = list(request.session["cart"])
        item_exist = next(
            (item for item in request.session["cart"] if item["id"] == int(request.POST.get("id"))),
            False,
        )
        json_data = {
            "id": int(request.POST.get("id")),
            "title": request.POST.get("title"),
            "qty": 1,
            "price": float(replace_to_dot(request.POST.get("price"))),
            "total_price_cart": float(replace_to_dot(request.POST.get("price"))) * 1,
        }
        if not item_exist:
            request.session["cart"].append(json_data)
            if request.session.get("wishlist"):
                for item in request.session["wishlist"]:
                    if item["id"] == int(request.POST.get("id")):
                        item.clear()
                    while {} in request.session["wishlist"]:
                        request.session["wishlist"].remove({})
                    if not request.session["wishlist"]:
                        del request.session["wishlist"]
            request.session.modified = True
        return JsonResponse(json_data, status=200)


def cart_delete_item(request):
    if request.method == "POST" and request.is_ajax():
        for item in request.session["cart"]:
            if item["id"] == int(request.POST.get("id")):
                item.clear()

        while {} in request.session["cart"]:
            request.session["cart"].remove({})

        if not request.session["cart"]:
            del request.session["cart"]

        request.session.modified = True
        price = float(replace_to_dot(request.POST.get("price")))
        json_data = {
            "id": int(request.POST.get("id")),
            "title": request.POST.get("title"),
            "qty": 1,
            "price": price,
            "total_price_cart": price * 1,
        }
        request.session.modified = True
        return JsonResponse(json_data)


def cart_delete_all(request):
    if request.session.get("cart"):
        del request.session["cart"]
    return redirect(request.POST.get("url_from"))
