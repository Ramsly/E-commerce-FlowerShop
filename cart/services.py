from decimal import Decimal


def replace_to_dot(price: float) -> Decimal:
    for i in price.replace(',', '.').split():
        price = i
    return price