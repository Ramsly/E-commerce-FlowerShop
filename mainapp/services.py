from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from django.contrib.postgres.search import (
    SearchQuery,
    SearchVector,
    SearchRank,
    SearchHeadline,
    TrigramSimilarity,
)

from .models import Product


def send_message_order(request, f_name, l_name, email, phone_number, buying_type, address, comment):
    subject, from_email, to = (
        "Venesia Flower Shop | Заказ №",
        "acperow.ram@yandex.ru",
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
    return msg.send()


def searched_products(q, category):
    vector = SearchVector("title")
    query = SearchQuery(q)
    search_headline = SearchHeadline("description", query)

    products_search = (
        Product.objects.annotate(rank=SearchRank(vector, query)).annotate(headline=search_headline).annotate(
            similarity=TrigramSimilarity("title", q),
        ).filter(similarity__gt=0.1, category=category).order_by("-rank")
    )
    if q is None:
        products_search = Product.objects.filter(category=category)

    return products_search
