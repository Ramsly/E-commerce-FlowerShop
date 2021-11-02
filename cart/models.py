from django.db import models
from django.conf import settings


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Пользователь", on_delete=models.CASCADE, related_name="user_for_cart")
    product = models.ForeignKey('mainapp.Product', on_delete=models.CASCADE, verbose_name="Товар", related_name="product_for_cart")
    quantity = models.IntegerField(default=1, verbose_name="Кол-во")

    class Meta:
        verbose_name_plural = "Корзина"

    def __str__(self):
        return f"{self.quantity} {self.product.title} {self.user.username}"
        
    @property
    def get_quantity_of_cart(self):
        return self.quantity

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_total_discount_product_price(self):
        return (self.product.price - (self.product.price / 100 * self.product.sale_value)) * self.quantity

    def get_final_price(self):
        if self.product.sale_value:
            return self.get_total_discount_product_price()
        return self.get_total_product_price()

# TODO: Сделать вывод товара из сессии и из БД 
# TODO: Добавить систему купонов
# TODO: Исправить поиск postgres
# TODO: AJAX
