from collections import defaultdict

from django import template
from django.utils.safestring import mark_safe

from specs.models import ProductFeatures

register = template.Library()


@register.filter
def product_spec(category):
    product_features = ProductFeatures.objects.filter(product__category=category)
    feature_and_values = defaultdict(list)
    for product_feature in product_features:
        if (
            product_feature.value
            not in feature_and_values[
                (
                    product_feature.feature.feature_name,
                    product_feature.feature.feature_filter_name,
                )
            ]
        ):
            feature_and_values[
                (
                    product_feature.feature.feature_name,
                    product_feature.feature.feature_filter_name,
                )
            ].append(product_feature.value)
    print(feature_and_values)
    search_filter_body = """<div class="filter__container">{}</div>"""
    mid_res = ""
    for (
        feature_name,
        feature_filter_name,
    ), feature_values in feature_and_values.items():
        feature_name_html = f"""<p class="padding">{feature_name}</p>"""
        feature_values_res = ""
        for f_v in feature_values:
            mid_feature_values_res = """  
    <label class='checkbox path'>
        <input type='checkbox' class='checkbox' name='{f_f_name}' value='{feature_name}'>
        {feature_name}
        <svg viewBox='0 0 21 21'>
           <path d='M5,10.75 L8.5,14.25 L19.4,2.3 C18.8333333,1.43333333 18.0333333,1 17,1 L4,1 C2.35,1 1,2.35 1,4 L1,17 C1,18.65 2.35,20 4,20 L17,20 C18.65,20 20,18.65 20,17 L20,7.99769186'></path>
        </svg>
    </label>""".format(
                feature_name=f_v, f_f_name=feature_filter_name
            )
            feature_values_res += mid_feature_values_res
        feature_name_html += feature_values_res
        mid_res += feature_name_html
    res = search_filter_body.format(mid_res)
    return mark_safe(res)