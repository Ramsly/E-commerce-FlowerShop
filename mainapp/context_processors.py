from .models import Category, Product

def products(request):
    return {'products': Product.objects.all()}


def categories(request):
    return {"categories": Category.objects.all()}


# def accounts(request, id):
#     return {"accounts": Account.objects.get(id=id)}


