from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.views.generic import DetailView, View, ListView, TemplateView

from specs.models import ProductFeatures
from .forms import ReviewForm, RatingForm
from .models import Category, Product, Rating

User = get_user_model()


class MyQ(Q):

    default = "OR"


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

    def get_user_stars(self, ip, product_id):
        if Rating.objects.filter(ip=ip, product_id=product_id).exists():
            stars = Rating.objects.get(ip=ip, product_id=product_id).star
        else:
            stars = None
        return stars

    def get(self, request, *args, **kwargs):

        ip = AddStarRating.get_client_ip(self, self.request)

        product_id = Product.objects.get(slug=kwargs['slug']).id
        stars = self.get_user_stars(ip, product_id)
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if stars:
            context['stars'] = str(stars)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        return context


class CategoryDetailView(DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = "category"
    template_name = "category_detail.html"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("search")
        category = self.get_object()
        context["categories"] = self.model.objects.all()
        if not query and not self.request.GET:
            context["category_products"] = category.product_set.all()
            return context
        if query:
            products = category.product_set.filter(Q(title__icontains=query))
            context["category_products"] = products
            return context
        url_kwargs = {}
        for item in self.request.GET:
            if len(self.request.GET.getlist(item)) > 1:
                url_kwargs[item] = self.request.GET.getlist(item)
            else:
                url_kwargs[item] = self.request.GET.get(item)
        q_condition_queries = Q()
        for key, value in url_kwargs.items():
            if isinstance(value, list):
                q_condition_queries.add(Q(**{"value__in": value}), Q.OR)
            else:
                q_condition_queries.add(Q(**{"value": value}), Q.OR)
        pf = (
            ProductFeatures.objects.filter(q_condition_queries)
            .prefetch_related("product", "feature")
            .values("product_id")
        )
        products = Product.objects.filter(id__in=[pf_["product_id"] for pf_ in pf])
        context["category_products"] = products
        return context


class CategoriesListView(ListView):

    model = Category
    context_object_name = "categories"
    template_name = "categories_detail.html"


class AboutUsView(TemplateView):

    template_name = "about.html"


class CheckoutView(TemplateView):
    
    template_name = "checkout.html"


class ReviewPageView(TemplateView):

    template_name = "reviews.html"


# class MakeOrderView(View):
#     @transaction.atomic
#     def post(self, request, *args, **kwargs):
#         form = OrderForm(request.POST or None)
#         customer = Customer.objects.get(user=request.user)
#         if form.is_valid():
#             new_order = form.save(commit=False)
#             new_order.customer = customer
#             new_order.first_name = form.cleaned_data["first_name"]
#             new_order.last_name = form.cleaned_data["last_name"]
#             new_order.phone = form.cleaned_data["phone"]
#             new_order.address = form.cleaned_data["address"]
#             new_order.buying_type = form.cleaned_data["buying_type"]
#             new_order.order_date = form.cleaned_data["order_date"]
#             new_order.comment = form.cleaned_data["comment"]
#             new_order.save()
#             # self.cart.in_order = True
#             request.session("cart").save()
#             new_order.cart = request.session("cart")
#             new_order.save()
#             customer.orders.add(new_order)
#             if request.session.get("cart"):
#                 del request.session["cart"]
#             messages.add_message(
#                 request, messages.INFO, "Спасибо за заказ! Менеджер с Вами свяжется"
#             )
#             return HttpResponseRedirect("/")
#         return HttpResponseRedirect("/checkout/")


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


class AddStarRating(View):
    """Добавление рейтинга фильму"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                product_id=int(request.POST.get("product")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)