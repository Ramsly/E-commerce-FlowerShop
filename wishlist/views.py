from django.shortcuts import redirect, render
from cart.utils import replace_to_dot
from mainapp.models import Product


def wishes(request):
    products = Product.objects.all()
    context = {
        "products": products,
        "wishes_session": request.session.get("wishlist"),
    }
    return render(request, "wishlist.html", context)


def wishes_add(request, id):
    if request.method == "POST":
        if not request.session.get("wishlist"):
            request.session["wishlist"] = list()
        else:
            request.session["wishlist"] = list(request.session["wishlist"])
        item_exist = next(
            (item for item in request.session["wishlist"] if item["id"] == request.POST.get("id")),
            False,
        )       
        add_data = {
            "id": request.POST.get("id"),
            "title": request.POST.get("title"),
            "qty": 1,
            "price": float(replace_to_dot(request.POST.get("price"))),
            "total_price_cart": float(replace_to_dot(request.POST.get("price"))) * 1,
        }
        if not item_exist:
            request.session["wishlist"].append(add_data)
            request.session.modified = True
    return redirect(request.POST.get("url_from"))


def wishes_delete_item(request, id):
    if request.method == "POST":
        for item in request.session["wishlist"]:
            if str(item["id"]) == str(request.POST.get("id")):
                item.clear()

        while {} in request.session["wishlist"]:
            request.session["wishlist"].remove({})

        if not request.session["wishlist"]:
            del request.session["wishlist"]

        request.session.modified = True
    return redirect(request.POST.get("url_from"))


def wishes_delete_all(request):
    if request.session.get("wishlist"):
        del request.session["wishlist"]
    return redirect(request.POST.get("url_from"))
