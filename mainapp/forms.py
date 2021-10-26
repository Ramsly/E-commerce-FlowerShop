from django import forms
from .models import Account
from .models import Reviews, RatingStar, Rating
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    """
    Form for Registering new users
    """

    email = forms.EmailField(
        max_length=60, help_text="Required. Add a valid email address"
    )
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,12}$', label="Телефон", error_messages={'invalid': 'Введите правильно номер телефона!'})

    class Meta:
        model = Account
        fields = ("username", "email", "f_name", "l_name", "phone_number","password1", "password2")

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)


class AccountAuthenticationForm(forms.ModelForm):
    """
    Form for Logging in  users
    """

    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ("email", "password")

    def __init__(self, *args, **kwargs):
        """
        specifying styles to fields
        """
        super(AccountAuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get("email")
            password = self.cleaned_data.get("password")
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Email или пароль введены неверно!")


# class AccountUpdateform(forms.ModelForm):
#     """
#     Updating User Info
#     """

#     class Meta:
#         model = Account
#         fields = ("email", "username")
#         widgets = {
#             "email": forms.TextInput(attrs={"class": "form-control"}),
#             "password": forms.TextInput(attrs={"class": "form-control"}),
#         }

#     def __init__(self, *args, **kwargs):
#         """
#         specifying styles to fields
#         """
#         super(AccountUpdateform, self).__init__(*args, **kwargs)
#         for field in (self.fields["email"], self.fields["username"]):
#             field.widget.attrs.update({"class": "form-control "})

#     def clean_email(self):
#         if self.is_valid():
#             email = self.cleaned_data["email"]
#             try:
#                 account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
#             except Account.DoesNotExist:
#                 return email
#             raise forms.ValidationError("Email '%s' already in use." % email)

#     def clean_username(self):
#         if self.is_valid():
#             username = self.cleaned_data["username"]
#             try:
#                 account = Account.objects.exclude(pk=self.instance.pk).get(
#                     username=username
#                 )
#             except Account.DoesNotExist:
#                 return username
#             raise forms.ValidationError("Username '%s' already in use." % username)


# class OrderForm(forms.Form):




class PostSearchForm(forms.Form):
    q = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["q"].label = "Поиск товара"


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
