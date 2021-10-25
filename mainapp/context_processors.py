from .models import Category, Product

def products(request):
    return {'products': Product.objects.all()}


def categories(request):
    return {"categories": Category.objects.all()}


