from .models import Category, Product
from .forms import OrderForm


def products(request):
    return {'products': Product.objects.all()}


def categories(request):
    return {"categories": Category.objects.all()}

