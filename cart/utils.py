def replace_to_dot(price):
    for i in price.replace(',', '.').split():
        price = i
    return price

