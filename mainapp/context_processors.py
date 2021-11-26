from django.db.models.aggregates import Sum
from .models import Category, Product, Like, Dislike


def products(request):
    return {"products": Product.objects.all()}


def categories(request):
    return {"categories": Category.objects.all()}



