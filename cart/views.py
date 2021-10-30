from django.core.checks import messages
from django.shortcuts import get_object_or_404, redirect, render
from .utils import replace_to_dot
from mainapp.models import Order, Product
from .models import OrderItem


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
            (
                item
                for item in request.session["cart"]
                if item["id"] == request.POST.get("id")
            ),
            False,
        )
        if not request.user.is_authenticated:
            data = {
                "id": request.POST.get("id"),
                "title": request.POST.get("title"),
                "qty": 1,
                "price": float(replace_to_dot(request.POST.get("price"))),
                "total_price_cart": float(replace_to_dot(request.POST.get("price")))
                * 1,
            }
            if not item_exist:
                request.session["cart"].append(data)
                if request.session.get("wishlist"):
                    for item in request.session["wishlist"]:
                        if item["id"] == request.POST.get("id"):
                            item.clear()
                        while {} in request.session["wishlist"]:
                            request.session["wishlist"].remove({})
                        if not request.session["wishlist"]:
                            del request.session["wishlist"]
                request.session.modified = True
        else:
            product = get_object_or_404(Product, id=id)
            order_item, created = OrderItem.objects.get_or_create(
                product=product, user=request.user, ordered=False
            )
            order_qs = Order.objects.filter(user=request.user)
            if order_qs.exists():
                order = order_qs[0]
                # check if the order item is in the order
                if order.products.filter(product__id=product.id).exists():
                    order_item.quantity += 1
                    order_item.save()
                    # messages.info(request, "This item quantity was updated.")
                    return redirect("/")
                else:
                    order.products.add(order_item)
                    # messages.INFO(request, "This item was added to your cart.")
                    return redirect("/")
            else:
                order = Order.objects.create(user=request.user)
                order.products.add(order_item)
                # messages.info(request, "This item was added to your cart.")
                return redirect("/")

    return redirect(request.POST.get("url_from"))


def cart_delete_item(request, id):
    if request.method == "POST":
        if not request.user.is_authenticated:
            for item in request.session["cart"]:
                if item["id"] == request.POST.get("id"):
                    item.clear()

            while {} in request.session["cart"]:
                request.session["cart"].remove({})

            if not request.session["cart"]:
                del request.session["cart"]

            request.session.modified = True
        else:
            product = get_object_or_404(Product, id=id)
            order_qs = Order.objects.filter(user=request.user, ordered=False)
            if order_qs.exists():
                order = order_qs[0]
                # check if the order item is in the order
                if order.items.filter(product__id=product.id).exists():
                    order_item = OrderItem.objects.filter(
                        product=product, user=request.user, ordered=False
                    )[0]
                    order.items.remove(order_item)
                    order_item.delete()
                    # messages.info(request, "This item was removed from your cart.")
                    return redirect("/")
                else:
                    # messages.info(request, "This item was not in your cart")
                    return redirect("/", id=id)
            else:
                # messages.info(request, "You do not have an active order")
                return redirect("/", id=id)
    return redirect(request.POST.get("url_from"))


def cart_delete_all(request):
    if request.session.get("cart"):
        del request.session["cart"]
    return redirect(request.POST.get("url_from"))
