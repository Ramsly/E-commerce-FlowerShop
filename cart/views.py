from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from .utils import *


def cart(request):
    context = {
        "cart_session": request.session.get("cart"),
    }
    return render(request, "cart.html", context)


def cart_add(request):
<<<<<<< HEAD
    if request.method == "POST" :
=======
    if request.method == "POST":
>>>>>>> 712e24a611dd456bd343730962eb195074440ca7
        if not request.session.get("cart"):
            request.session["cart"] = list()
        else:
            request.session["cart"] = list(request.session["cart"])
        item_exist = next(
            (item for item in request.session["cart"] if item["id"] == int(id)),
            False,
        )
        price = float(replace_to_dot(request.POST.get("price")))
        app_data = {
            "id": int(id),
            "title": request.POST.get("title"),
            "qty": 1,
            "price": price,
            "total_price_cart": price * 1
        }
        if not item_exist:
            request.session["cart"].append(app_data)
            if request.session.get('wishlist'):
                for item in request.session["wishlist"]:
                    if item["id"] == int(id):
                        item.clear()
                    while {} in request.session["wishlist"]:
                        request.session["wishlist"].remove({})
                    if not request.session["wishlist"]:
                        del request.session["wishlist"]
            request.session.modified = True
<<<<<<< HEAD
    if request.is_ajax():
        json_data = {
            "id": int(id),
            "title": request.POST.get("title"),
            "qty": 1,
            "price": price,
            "total_price_cart": price * 1
        }
        request.session.modified = True
        return JsonResponse(json_data)
=======
        return JsonResponse(add_data)
>>>>>>> 712e24a611dd456bd343730962eb195074440ca7
    return redirect(request.POST.get("url_from"))


# def cart_add_qty(request):
#     if request.method == "POST" and request.is_ajax():
#         for item in request.session["cart"]:
#             if item["id"] == int(id):



def cart_delete_item(request):
    if request.method == "POST":
        for item in request.session["cart"]:
            if item["id"] == int(id):
                item.clear()

        while {} in request.session["cart"]:
            request.session["cart"].remove({})

        if not request.session["cart"]:
            del request.session["cart"]

        request.session.modified = True
    if request.is_ajax():
        price = float(replace_to_dot(request.POST.get("price")))
        json_data = {
            "id": int(id),
            "title": request.POST.get("title"),
            "qty": 1,
            "price": price,
            "total_price_cart": price * 1
        }
        request.session.modified = True
        return JsonResponse(json_data)
    return redirect(request.POST.get("url_from"))


def cart_delete_all(request):
    if request.session.get("cart"):
        del request.session["cart"]
    return redirect(request.POST.get("url_from"))
