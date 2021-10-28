from django.db import models
from mainapp.models import Account, Product


class Wishlist(models.Model):
    user = models.ForeignKey(Account, verbose_name="Покупатель", on_delete=models.CASCADE, null=False, blank=False)
    product = models.ManyToManyField(
        Product, verbose_name="Товары", blank=True
    )
    qty = models.SmallIntegerField(
        verbose_name="Кол-во товаров в корзине", default=0
    )
    price = models.DecimalField(verbose_name="Цена", max_digits=6, default=0, decimal_places=2)

    class Meta:
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Желания: {self.user}"
