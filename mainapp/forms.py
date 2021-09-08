from django import forms
from django.contrib.auth import get_user_model
from .models import Reviews, RatingStar, Rating

User = get_user_model()

# class LoginForm(forms.ModelForm):

#     password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ["username", "password"]

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["username"].label = "Логин"
#         self.fields["password"].label = "Пароль"

#     def clean(self):
#         username = self.cleaned_data["username"]
#         password = self.cleaned_data["password"]
#         if not User.objects.filter(username=username).exists():
#             raise forms.ValidationError(
#                 f'Пользователь с логином "{username} не найден в системе'
#             )
#         user = User.objects.filter(username=username).first()
#         if user:
#             if not user.check_password(password):
#                 raise forms.ValidationError("Неверный пароль")
#         return self.cleaned_data


# class RegistrationForm(forms.ModelForm):

#     confirm_password = forms.CharField(widget=forms.PasswordInput)
#     password = forms.CharField(widget=forms.PasswordInput)
#     phone = forms.CharField(required=False)
#     address = forms.CharField(required=False)
#     email = forms.EmailField(required=True)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["username"].label = "Логин"
#         self.fields["password"].label = "Пароль"
#         self.fields["confirm_password"].label = "Подтвердите пароль"
#         self.fields["phone"].label = "Номер телефона"
#         self.fields["first_name"].label = "Имя"
#         self.fields["last_name"].label = "Фамилия"
#         self.fields["address"].label = "Адрес"
#         self.fields["email"].label = "Электронная почта"

#     def clean_email(self):
#         email = self.cleaned_data["email"]
#         domain = email.split(".")[-1]
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError(
#                 f"Данный почтовый адрес уже зарегистрирован в системе"
#             )
#         return email

#     def clean_username(self):
#         username = self.cleaned_data["username"]
#         if User.objects.filter(username=username).exists():
#             raise forms.ValidationError(f"Имя {username} занято")
#         return username

#     def clean(self):
#         password = self.cleaned_data["password"]
#         confirm_password = self.cleaned_data["confirm_password"]
#         if password != confirm_password:
#             raise forms.ValidationError("Пароли не совпадают")
#         return self.cleaned_data

#     class Meta:
#         model = User
#         fields = [
#             "username",
#             "email",
#             "password",
#             "confirm_password",
#             "first_name",
#             "last_name",
#             "address",
#             "phone",
#         ]

# class OrderForm(forms.Form):
#     """Форма заказа (отправка Email)"""

#     BUYING_TYPE_SELF = 'self'
#     BUYING_TYPE_DELIVERY = 'delivery'
#     BUYING_TYPE_CHOICES = (
#         (BUYING_TYPE_SELF, 'Самовывоз'),
#         (BUYING_TYPE_DELIVERY, 'Доставка')
#     )

#     first_name = forms.CharField(label="Имя")
#     last_name = forms.CharField(label="Фамилия")
#     telephone = forms.IntegerField(label="Номер телефона")
#     email = forms.EmailField(label="Email")
#     buying_type = forms.ChoiceField(
#         label='Тип заказа',
#         choices=BUYING_TYPE_CHOICES,
#     )
#     address = forms.CharField(label='Адрес')
#     comment = forms.CharField(label='Комментарий к заказу')
#     product = forms.CharField()


class ReviewForm(forms.ModelForm):
    """Форма отзывов"""

    class Meta:
        model = Reviews
        fields = ("comment", "name")


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star",)

