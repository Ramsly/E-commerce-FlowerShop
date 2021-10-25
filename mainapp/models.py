from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator

User = get_user_model()


# manager for our custom model
class MyAccountManager(BaseUserManager):
    """
    This is a manager for Account class
    """

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an Emaill address")
        if not username:
            raise ValueError("Users must have an Username")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):

    """
    Custom user class inheriting AbstractBaseUser class
    """

    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    phone_number = models.CharField(verbose_name="Телефон", validators=[phone_regex], max_length=15, blank=True) # validators should be a list
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Customer(models.Model):

    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    f_name = models.CharField(verbose_name="Имя", max_length=255, default="")
    l_name = models.CharField(verbose_name="Фамилия", max_length=255, default="")
    image = models.ImageField(verbose_name="Изображение", blank=True, null=True)
    email = models.EmailField(verbose_name="Почта", blank=True, null=True)
    phone = models.CharField(
        max_length=20, verbose_name="Номер телефона", null=True, blank=True
    )
    address = models.CharField(
        max_length=255, verbose_name="Адрес", null=True, blank=True
    )
    slug = models.SlugField(unique=False, default="", blank=True, null=True)

    def __str__(self):
        return f"{self.address}"

    def get_absolute_url(self):
        return reverse("customer", kwargs={"slug": self.slug})

    class Meta:
        verbose_name_plural = "Покупатели"


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
        Category, verbose_name="Категория", on_delete=models.CASCADE, default=""
    )
    title = models.CharField(verbose_name="Наименование", max_length=255, db_index=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name="Изображение", upload_to="flowers/")
    description = models.TextField(verbose_name="Описание", null=True)
    price = models.FloatField(verbose_name="Цена", default=0)
    features = models.ManyToManyField(
        "specs.ProductFeatures", blank=True, related_name="features_for_product"
    )
    shipping_price = models.IntegerField(verbose_name="Стоимость доставки", default=0)
    sale_value = models.FloatField(
        verbose_name="Величина скидки",
        default=0,
        help_text="В процентах. Значок процента не ставить!",
    )
    available = models.BooleanField(verbose_name="Наличие товара", default=True)

    def __str__(self):
        return f"{self.title}"

    @property
    def get_total_sale(self):
        total = self.price - (self.price / 100 * self.sale_value)
        return total

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Товары"
        verbose_name_plural = "Товары"


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
    product = models.ForeignKey(
        Product, verbose_name="Цветы", on_delete=models.CASCADE, null=True, default=""
    )

    def __str__(self):
        return f"{self.name} - {self.product}"

    class Meta:
        verbose_name_plural = "Отзывы"
        ordering = ["-time"]


class RatingStar(models.Model):
    """Звезда рейтинга"""

    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f"{self.value}"

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг"""

    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(
        RatingStar, on_delete=models.CASCADE, verbose_name="Звезда", default=0
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Товар", default=""
    )

    def __str__(self):
        return f"{self.star} - {self.product}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"