from django import template
from django.shortcuts import get_object_or_404
from mainapp.models import Like, Dislike, Product
from cart.models import OrderItem
from django.db.models.aggregates import Sum
from django.db.models import Count

register = template.Library()


@register.filter
def count_likes(id):
    product = get_object_or_404(Product, id=id)
    count_likes = (
        Like.objects.filter(products=product)
        .aggregate(count_likes=Count("products"))
        .get("count_likes")
    )
    return count_likes

@register.filter
def count_dislikes(id):
    product = get_object_or_404(Product, id=id)
    count_dislikes = (
        Dislike.objects.filter(products=product)
        .aggregate(count_dislikes=Count("products"))
        .get("count_dislikes")
    )
    return count_dislikes