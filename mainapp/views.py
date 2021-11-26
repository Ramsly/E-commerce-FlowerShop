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
    ReviewForm,
    RegistrationForm,
    AccountAuthenticationForm,
    OrderForm,
)

from .models import Category, Dislike, Like, Order, Product
from cart.models import OrderItem

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


class CategoryListView(ListView):
    def get(self, request, slug, *args, **kwargs):
        products = Product.objects.all()
        q = request.GET.get("q")

        if slug:
            category = get_object_or_404(Category, slug=slug)
            products_of_category = products.filter(category=category)

        if q:
            vector = SearchVector("title")
            query = SearchQuery(q)
            search_headline = SearchHeadline("description", query)

            products_search = (
                Product.objects.annotate(rank=SearchRank(vector, query))
                .annotate(headline=search_headline)
                .annotate(
                    similarity=TrigramSimilarity("title", q),
                )
                .filter(similarity__gt=0.1, category=category)
                .order_by("-rank")
            )
        else:
            products_search = products.filter(category=category)
            messages.add_message(request, messages.ERROR, "Ничего не найдено!")

        context = {
            "products_of_category": products_of_category,
            "category": category,
            "products_search": products_search,
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


class OrderView(View):
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
                if not request.user.is_authenticated:
                    del request.session["cart"]
                    request.session.modified = True
                order_qs = Order.objects.filter(user=request.user)
                if order_qs.exists():
                    order = order_qs[0]
                    if order.products_cart.filter(user=request.user).exists():
                        order_item = OrderItem.objects.filter(user=request.user)
                        order.delete()
                        order_item.delete()
            except BadHeaderError:
                return HttpResponse("Плохое соединение")
            messages.success(request, "Спасибо за заказ!")
            return redirect("/")
        context = {"form": form}
        return render(request, "order.html", context)


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
                if request.session.get("cart"):
                    del request.session["cart"]
                    request.session.modified = True
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
            shipping_address = form.cleaned_data("shipping_address")
            phone_number = form.cleaned_data.get("phone_number")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            if request.session.get("cart"):
                del request.session["cart"]
                request.session.modified = True
            account = authenticate(email=email, password=password)
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

    def post(self, request, slug, *args, **kwargs):
        form = ReviewForm(request.POST)
        product = Product.objects.get(slug=slug)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.product = product
            form.save()
        return HttpResponseRedirect(product.get_absolute_url())


class LikeView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, id, *args, **kwargs):
        product = get_object_or_404(Product, id=id)
        like = Like.objects.filter(user=request.user, products=product)
        dislike = Dislike.objects.filter(user=request.user, products=product)
        if not like.exists():
            if not dislike.exists():
                like = Like.objects.create(user=request.user, products=product)
                return redirect(request.POST.get("url_from"))
            else:
                dislike = Dislike.objects.get(user=request.user, products=product)
                dislike.delete()
                like = Like.objects.create(user=request.user, products=product)
        else:
            like = Like.objects.get(user=request.user, products=product)
            like.delete()
        return redirect(request.POST.get("url_from"))


class DislikeView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, id, *args, **kwargs):
        product = get_object_or_404(Product, id=id)
        like = Like.objects.filter(user=request.user, products=product)
        dislike = Dislike.objects.filter(user=request.user, products=product)
        if not dislike.exists():
            if not like.exists():
                dislike = Dislike.objects.create(user=request.user, products=product)
                return redirect(request.POST.get("url_from"))
            else:
                like = Like.objects.get(user=request.user, products=product)
                like.delete()
                dislike = Dislike.objects.create(user=request.user, products=product)
        else:
            dislike = Dislike.objects.get(user=request.user, products=product)
            dislike.delete()
        return redirect(request.POST.get("url_from"))
