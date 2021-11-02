from django.shortcuts import redirect, render
from django.core.checks import messages
from django.shortcuts import get_object_or_404, redirect, render
from cart.utils import replace_to_dot
from django.http import JsonResponse
from mainapp.models import Product, Order
from .models import OrderItem
from django.views.generic import TemplateView, View


class WishesView(TemplateView):

    template_name = "wishlist.html"


class AddProductToWishesView(View):
    def post(self, request, id, *args, **kwargs):
        if not request.user.is_authenticated:
            if not request.session.get("wishlist"):
                request.session["wishlist"] = list()
            else:
                request.session["wishlist"] = list(request.session["wishlist"])
            item_exist = next(
                (
                    item
                    for item in request.session["wishlist"]
                    if item["id"] == request.POST.get("id")
                ),
                False,
            )
            data = {
                "id": request.POST.get("id"),
                "title": request.POST.get("title"),
                "qty": 1,
                "price": float(replace_to_dot(request.POST.get("price"))),
                "total_price_cart": float(replace_to_dot(request.POST.get("price")))
                * 1,
            }
            if not item_exist:
                request.session["wishlist"].append(data)
                request.session.modified = True
        else:
            product = get_object_or_404(Product, id=id)
            order_item, created = OrderItem.objects.get_or_create(
                product=product, user=request.user
            )
            order_qs = Order.objects.filter(user=request.user)
            if order_qs.exists():
                order = order_qs[0]
                # check if the order item is in the order
                if order.products_wishlist.filter(product__id=product.id).exists():
                    order_item.quantity += 1
                    order_item.save()
                    # messages.info(request, "This item quantity was updated.")
                    return redirect("/")
                else:
                    order.products_wishlist.add(order_item)
                    # messages.info(request, "This item was added to your cart.")
                    return redirect("/")
            else:
                order = Order.objects.create(user=request.user)
                order.products_wishlist.add(order_item)
                # messages.info(request, "This item was added to your cart.")
                return redirect("/")
        return redirect(request.POST.get("url_from"))


class DeleteProductFromWishesView(View):
    def post(request, id, *args, **kwargs):
        if request.user.is_authenticated:
            for item in request.session["wishlist"]:
                if str(item["id"]) == str(request.POST.get("id")):
                    item.clear()

            while {} in request.session["wishlist"]:
                request.session["wishlist"].remove({})

            if not request.session["wishlist"]:
                del request.session["wishlist"]

            request.session.modified = True
        else:
            product = get_object_or_404(Product, id=id)
            order_qs = Order.objects.filter(user=request.user)
            if order_qs.exists():
                order = order_qs[0]
                # check if the order item is in the order
                if order.products_wishlist.filter(product__id=product.id).exists():
                    order_item = OrderItem.objects.filter(
                        product=product, user=request.user
                    )[0]
                    if order_item.quantity > 1:
                        order_item.quantity -= 1
                        order_item.save()
                    else:
                        order.products_wishlist.remove(order_item)
                    # messages.info(request, "This item quantity was updated.")
                    return redirect("/")
                else:
                    # messages.info(request, "This item was not in your cart")
                    return redirect("/", id=id)
        return redirect(request.POST.get("url_from"))


class DeleteAllProductsFromWishesView(View):
    def post(self, request, id, *args, **kwargs):
        if request.session.get("wishlist") and not request.user.is_authenticated:
            del request.session["wishlist"]
        else:
            product = get_object_or_404(Product, id=id)
            order_qs = Order.objects.filter(user=request.user)
            if order_qs.exists():
                order = order_qs[0]
                # check if the order item is in the order
                if order.products_wishlist.filter(product__id=product.id).exists():
                    order_item = OrderItem.objects.filter(
                        product=product, user=request.user
                    )[0]
                    order.products_wishlist.remove(order_item)
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
