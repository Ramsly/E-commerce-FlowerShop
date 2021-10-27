from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.http.response import BadHeaderError, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.generic import DetailView, View, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    PostSearchForm,
    ReviewForm,
    RegistrationForm,
    AccountAuthenticationForm,
    OrderForm,
)
from .models import Account, Category, Product

from django.contrib.postgres.search import (
    SearchQuery,
    SearchVector,
    SearchRank,
    SearchHeadline,
    TrigramSimilarity,
)


class AboutUsView(TemplateView):

    template_name = "about.html"


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
                return q

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


# class CustomerDetailView(DetailView, LoginRequiredMixin):

#     model = Customer
#     context_object_name = "customer"
#     slug_url_kwarg = "slug"
#     template_name = "profile_detail.html"


class SendToEmailOrderView(View):
    def get(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        context = {"form": form}
        return render(request, "order.html", context)

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        if form.is_valid():
            f_name = form.cleaned_data.get("f_name")
            l_name = form.cleaned_data.get("l_name")
            email = form.cleaned_data.get("email")
            phone_number = form.cleaned_data.get("phone_number")
            buying_type = form.cleaned_data.get("buying_type")
            address = form.cleaned_data.get("address")
            comment = form.cleaned_data.get("comment")
            subject, from_email, to = (
                "Venesia Flower Shop | Заказ №",
                "theluckyfeed1@gmail.com",
                f"{email}",
            )
            text_content = ""
            data = {
                "f_name": f_name,
                "l_name": l_name,
                "email": email,
                "phone_number": phone_number,
                "buying_type": buying_type,
                "address": address,
                "comment": comment,
                "products": request.POST.get("product"),
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
            return redirect("/")
        context = {"form": form}
        return render(request, "order.html", context)

    # def post(self, request, *args, **kwargs):
    #     subject, from_email, to = (
    #         "Venesia Flower Shop | Заказ №",
    #         "theluckyfeed1@gmail.com",
    #         f'{request.POST.get("email")}',
    #     )
    #     text_content = ""
    #     data = {
    #         "first_name": request.POST.get("first_name"),
    #         "last_name": request.POST.get("last_name"),
    #         "telephone": request.POST.get("telephone"),
    #         "email": request.POST.get("email"),
    #         "buying_type": request.POST.get("buying_type"),
    #         "address": request.POST.get("address"),
    #         "comment": request.POST.get("comment"),
    #         "order": request.POST.get("product"),
    #     }
    #     html_content = render_to_string("html_email.html", data)
    #     msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    #     msg.attach_alternative(html_content, "text/html")
    #     try:
    #         msg.send()
    #         del request.session["cart"]
    #         request.session.modified = True
    #     except BadHeaderError:
    #         return HttpResponse("Плохое соединение")
    #     messages.success(request, "Спасибо за заказ!")
    #     return HttpResponseRedirect("/")


class AccountAuthenticationView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        form = AccountAuthenticationForm(request.POST or None)
        context = {
            "form": form,
        }
        return render(request, "login.html", context)

    def post(self, request, *args, **kwargs):
        form = AccountAuthenticationForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, "Вы авторизированны!")
                return redirect("/")
            else:
                messages.error("Пожалуйста исправьте ошибки!")
        context = {
            "form": form,
        }
        return render(request, "login.html", context)


class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        form = RegistrationForm(request.POST or None)
        context = {
            "form": form,
        }
        return render(request, "registration.html", context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            form.save()
            f_name = form.cleaned_data.get("f_name")
            l_name = form.cleaned_data.get("l_name")
            phone_number = form.cleaned_data.get("phone_number")
            email = form.cleaned_data.get("email")
            raw_pass = form.cleaned_data.get("password1")
            account = authenticate(email=email, password=raw_pass)
            login(request, account)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect("/")
        else:
            messages.error(request, "Пожалуйста исправьте ошибки!")
        context = {
            "form": form,
        }
        return render(request, "registration.html", context)


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
