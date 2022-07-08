def replace_to_dot(price: float) -> float:
    for i in price.replace(',', '.').split():
        price = i
    return price