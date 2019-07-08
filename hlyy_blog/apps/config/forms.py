from django import forms

from .models import Subscribe
from util.forms import FormMixin


class SubscribeForm(forms.ModelForm, FormMixin):
    class Meta:
        model = Subscribe
        fields = ['email']