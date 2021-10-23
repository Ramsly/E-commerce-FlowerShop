from django.contrib.auth import authenticate, get_user_model, login
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.http.response import BadHeaderError, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.generic import DetailView, View, ListView, TemplateView
from specs.models import ProductFeatures
from .forms import PostSearchForm, ReviewForm, Authentificate
from .models import Category, Product, Customer

from django.contrib.postgres.search import (
    SearchQuery,
    SearchVector,
    SearchRank,
    SearchHeadline,
    TrigramSimilarity,
)

User = get_user_model()


class AboutUsView(TemplateView):

    template_name = "about.html"


class CheckoutView(TemplateView):

    template_name = "checkout.html"


class ReviewPageView(TemplateView):

    template_name = "reviews.html"


class BaseView(ListView):

    paginate_by = 10
    model = Product
    context_object_name = "products"
    template_name = "base.html"


class ProductDetailView(DetailView):

    model = Product
    context_object_name = "product"
    template_name = "product_detail.html"
    slug_url_kwarg = "slug"


class CategoryListView(View):
    def get(self, request, slug, *args, **kwargs):
        products_of_category = Product.objects.all()
        category = None
        q = request.GET.get("q")
        form = PostSearchForm

        results = []

        if slug:
            category = get_object_or_404(Category, slug=slug)
            products_of_category = products_of_category.filter(category=category)

        if "q" in request.GET:
            form = PostSearchForm(request.GET)

            if form.is_valid():
                q = form.cleaned_data["q"]
                results = Product.objects.annotate(
                    search=SearchVector("title"),
                ).filter(search=q)

        context = {
            "products_of_category": products_of_category,
            "category": category,
            "form": form,
            "results": results,
            "q": q,
        }
        return render(request, "category_detail.html", context)


class CategoriesListView(ListView):

    model = Category
    context_object_name = "categories"
    template_name = "categories_detail.html"


class CustomerDetailView(DetailView):

    model = Customer
    context_object_name = "customer"
    slug_url_kwarg = "slug"
    template_name = "profile_detail.html"


class SendToEmailOrderView(View):
    def post(self, request, *args, **kwargs):
        subject, from_email, to = (
            "Venesia Flower Shop | Заказ №",
            "theluckyfeed1@gmail.com",
            f'{request.POST.get("email")}',
        )
        text_content = ""
        data = {
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "telephone": request.POST.get("telephone"),
            "email": request.POST.get("email"),
            "buying_type": request.POST.get("buying_type"),
            "address": request.POST.get("address"),
            "comment": request.POST.get("comment"),
            "order": request.POST.get("product"),
        }
        html_content = render_to_string("html_email.html", data)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()
            del request.session["cart"]
            request.session.modified = True
        except BadHeaderError:
            return HttpResponse("Плохое соединение")
        messages.success(request, "Спасибо за заказ!")
        return HttpResponseRedirect("/")


class AuthentificationView(View):
    def get(self, request, *args, **kwargs):
        form = Authentificate(request.POST or None)
        context = {
            "form": form,
        }
        return render(request, "authentification.html", context)

    def post(self, request, *args, **kwargs):
        form = Authentificate(request.POST or None)
        if form.is_valid():
            if not Customer.objects.filter(phone_number=form.cleaned_data['phone_number']).exists():
                new_user = form.save(commit=False)
                new_user.phone_number = form.cleaned_data["phone_number"]
                new_user.save()
                Customer.objects.create(phone_number=form.cleaned_data["phone_number"])
                user = authenticate(phone_number=new_user.phone_number)
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                phone_number = form.cleaned_data["phone_number"]
                user = authenticate(phone_number=phone_number)
                login(request, user)
                return HttpResponseRedirect("/")
        context = {
            "form": form,
        }
        return render(request, "authentification.html", context)


class AddReviewToProduct(View):
    """Отзывы"""

    def post(self, request, slug):
        form = ReviewForm(request.POST)
        product = Product.objects.get(slug=slug)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.product = product
            form.save()
        return HttpResponseRedirect(product.get_absolute_url())


# class AddStarRating(View):
#     """Добавление рейтинга фильму"""
