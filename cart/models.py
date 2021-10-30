from django.conf import settings
from django.db import models


class OrderItem(models.Model): # * Cart
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Пользователь", on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey('mainapp.Product', on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.IntegerField(default=1, verbose_name="Кол-во")

    class Meta:
        verbose_name_plural = "Корзина"

    def __str__(self):
        return f"{self.quantity} {self.product.title} {self.user.username}"

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_total_discount_product_price(self):
        return (self.product.price - (self.product.price / 100 * self.product.sale_value)) * self.quantity

    def get_final_price(self):
        if self.product.sale_value:
            return self.get_total_discount_product_price()
        return self.get_total_product_price()


# TODO: Delete Cart page and custom Order
# TODO: Make a cart with relationship Account
# TODO: Make a wishlist with relationship Account
# TODO: AJAX cart and wishlist
# TODO: Repair postgres search
# TODO: Add coupon system
# TODO: FBV to CBV in cart and wishlist
# TODO: Make form in forms.py to add products cart and wishlist (form.cleaned_data.get())
