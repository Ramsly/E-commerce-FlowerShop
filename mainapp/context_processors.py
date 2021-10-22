from .models import Category, Customer, Product

def products(request):
    return {'products': Product.objects.all()}


def categories(request):
    return {"categories": Category.objects.all()}


def customers(request):
    return {"customers": Customer.objects.all()}

