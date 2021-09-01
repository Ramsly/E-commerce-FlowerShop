from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    BaseView,
    ProductDetailView,
    CategoryDetailView,
    CategoriesListView,
    CheckoutView,
    SendToEmailOrderView,
    # LoginView,
    # RegistrationView,
    AddReviewToProduct,
    AboutUsView,
    ReviewPageView,
)


urlpatterns = [
    path("", BaseView.as_view(), name="base"),
    path("products/<str:slug>/", ProductDetailView.as_view(), name="product_detail"),
    path("category/<str:slug>/", CategoryDetailView.as_view(), name="category_detail"),
    path("categories/", CategoriesListView.as_view(), name="categories"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("make-order/", SendToEmailOrderView.as_view(), name="make_order"),
    path("about/", AboutUsView.as_view(), name="about"),
    path("review/<str:slug>/", AddReviewToProduct.as_view(), name="add_review"),
    path("reviews/", ReviewPageView.as_view(), name="reviews"),
    # path("login/", LoginView.as_view(), name="login"),
    # path("registration/", RegistrationView.as_view(), name="registration"),
    # path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
]
