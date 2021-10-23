from django import forms
from django.contrib.auth import get_user_model
from .models import Reviews, RatingStar, Rating, Customer

User = get_user_model()

class Authentificate(forms.ModelForm):

    class Meta: 
        model = Customer
        fields = ("phone_number",)

    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$')


class PostSearchForm(forms.Form):
    q = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['q'].label = "Поиск товара"


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

