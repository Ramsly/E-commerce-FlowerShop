from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name="Имя категории")
    image = models.ImageField(
        verbose_name="Изображение категории", blank=True, null=True
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name_plural = "Категории"


class Product(models.Model):
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255, verbose_name="Наименование")
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name="Изображение", upload_to="flowers/")
    description = models.TextField(verbose_name="Описание", null=True)
    price = models.FloatField(verbose_name="Цена", default=0)
    features = models.ManyToManyField(
        "specs.ProductFeatures", blank=True, related_name="features_for_product"
    )
    freeship = models.BooleanField(
        verbose_name="Бесплатная доставка",
        default=False,
    )
    shipping_price = models.IntegerField(
        verbose_name="Стоимость доставки",
        default=0
    )
    sale = models.BooleanField(
        verbose_name="Акция",
        default=False,
    )
    sale_value = models.FloatField(
        verbose_name="Величина скидки",
        default=0,
        help_text="В процентах. Значок процента не ставить!",
    )
    available = models.BooleanField(verbose_name="Наличие товара", default=True)

    def __str__(self):
        return f"{self.title} | {self.id}"

    @property
    def get_total_sale(self):
        total = self.price - (self.price / 100 * self.sale_value)
        return total

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    def get_features(self):
        return {
            f.feature.feature_name: " ".join([f.value, f.feature.unit or ""])
            for f in self.features.all()
        }

    class Meta:
        verbose_name = "Товары"
        verbose_name_plural = "Товары"

# class Customer(models.Model):

#     user = models.ForeignKey(
#         User, verbose_name="Пользователь", on_delete=models.CASCADE
#     )
#     image = models.ImageField(verbose_name="Изображение", blank=True, null=True)
#     email = models.EmailField(verbose_name="Почта", blank=True, null=True)
#     phone = models.CharField(
#         max_length=20, verbose_name="Номер телефона", null=True, blank=True
#     )
#     address = models.CharField(
#         max_length=255, verbose_name="Адрес", null=True, blank=True
#     )
#     slug = models.SlugField(unique=True)

#     def __str__(self):
#         return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)

#     def get_absolute_url(self):
#         return reverse("customer", kwargs={"slug": self.slug})

#     class Meta:
        # verbose_name_plural = "Покупатели"


class Reviews(models.Model):
    time = models.DateTimeField(
        verbose_name="Дата комментария",
        blank=True,
        null=True,
        auto_created=True,
        auto_now=datetime.now(),
    )
    name = models.CharField("Имя", max_length=100, null=True)
    comment = models.TextField("Комментарий", max_length=5000, null=True)
    parent = models.ForeignKey(
        "self",
        verbose_name="Родитель",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    product = models.ForeignKey(Product, verbose_name="Цветы", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name} - {self.product}"

    class Meta:
        verbose_name_plural = "Отзывы"
        ordering = ["-time"]


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="Звезда")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")

    def __str__(self):
        return f"{self.star} - {self.product}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"