from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.http.response import BadHeaderError, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.generic import DetailView, View, ListView, TemplateView
from .forms import OrderForm 
from django.contrib.postgres.search import (
    SearchQuery,
    SearchVector,
    SearchRank,
    SearchHeadline,
)

from specs.models import ProductFeatures
from .forms import ReviewForm, RatingForm, OrderForm
from .models import Category, Product, Rating

User = get_user_model()


class BaseView(ListView):

    paginate_by = 12
    model = Product
    context_object_name = "products"
    template_name = "base.html"


class ProductDetailView(DetailView):

    model = Product
    context_object_name = "product"
    template_name = "product_detail.html"
    slug_url_kwarg = "slug"


class CategoryDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        products_of_category = Product.objects.all()
        category = None
        q = request.GET.get("q")

        if slug:
            category = get_object_or_404(Category, slug=slug)
            products_of_category = products_of_category.filter(category=category)
        if q:
            vector = SearchVector("slug")
            query = SearchQuery(q)

            search_products = products_of_category.annotate(search=vector).filter(
                search=query, category=category
            )
        else:
            search_products = products_of_category.filter(category=category)

        context = {
            "products_of_category": products_of_category,
            "category": category,
            "search_products": search_products,
        }
        return render(request, "category_detail.html", context)


class CategoriesListView(ListView):

    model = Category
    context_object_name = "categories"
    template_name = "categories_detail.html"


class AboutUsView(TemplateView):

    template_name = "about.html"


class CheckoutView(TemplateView):

    template_name = "checkout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = OrderForm()
        return context


class ReviewPageView(TemplateView):

    template_name = "reviews.html"


class SendToEmailOrderView(View):
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        if form.is_valid():
            subject, from_email, to = (
                "Venesia Flower Shop | Заказ №",
                "theluckyfeed1@gmail.com",
                f'{request.POST.get("email")}',
            )
            text_content = ""
            data = {
                "first_name": form.cleaned_data['first_name'],
                "last_name": form.cleaned_data["last_name"],
                "telephone": form.cleaned_data["telephone"],
                "email": form.cleaned_data["email"],
                "buying_type": form.cleaned_data["buying_type"],
                "address": form.cleaned_data["address"],
                "comment": form.cleaned_data["comment"],
                "order": request.POST.get("product"),
            }
            html_content = render_to_string("html_email.html", data)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except BadHeaderError:
                return HttpResponse("Плохое соединение")
            messages.success(request, "Спасибо за заказ!")
            return redirect("/")
        messages.error(request, "Заполните все поля!")
        form = OrderForm()
        return render(request, "checkout.html", {"form": form})


# class LoginView(View):

#     def get(self, request, *args, **kwargs):
#         form = LoginForm(request.POST or None)
#         context = {
#             'form': form,
#         }
#         return render(request, 'login.html', context)

#     def post(self, request, *args, **kwargs):
#         form = LoginForm(request.POST or None)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(
#                 username=username, password=password
#             )
#             if user:
#                 login(request, user)
#                 return HttpResponseRedirect('/')
#         context = {
#             'form': form,
#         }
#         return render(request, 'login.html', context)


# class RegistrationView(View):

#     def get(self, request, *args, **kwargs):
#         form = RegistrationForm(request.POST or None)
#         context = {
#             'form': form,
#         }
#         return render(request, 'registration.html', context)

#     def post(self, request, *args, **kwargs):
#         form = RegistrationForm(request.POST or None)
#         if form.is_valid():
#             new_user = form.save(commit=False)
#             new_user.username = form.cleaned_data['username']
#             new_user.email = form.cleaned_data['email']
#             new_user.first_name = form.cleaned_data['first_name']
#             new_user.last_name = form.cleaned_data['last_name']
#             new_user.save()
#             new_user.set_password(form.cleaned_data['password'])
#             new_user.save()
#             Customer.objects.create(
#                 user=new_user,
#                 phone=form.cleaned_data['phone'],
#                 address=form.cleaned_data['address']
#             )
#             user = authenticate(
#                 username=new_user.username, password=form.cleaned_data['password']
#             )
#             login(request, user)
#             return HttpResponseRedirect('/')
#         context = {
#             'form': form,
#         }
#         return render(request, 'registration.html', context)


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
