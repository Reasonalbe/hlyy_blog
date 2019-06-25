from django import forms
from django.forms import widgets

from .models import Comments


class CommentForm(forms.ModelForm):
    nickname = forms.CharField(
        label='昵称',
        max_length=50,
        required=True,
        widget=widgets.Input(
            attrs={
                'class': 'form-control',
                'style': 'width: 60%',
            }
        )
    )
    email = forms.CharField(
        label='Email',
        max_length=50,
        required=False,
        widget=widgets.Input(
            attrs={
                'class': 'form-control',
                'style': 'width: 60%',
            }
        )
    )
    website = forms.CharField(
        label='网站',
        max_length=200,
        required=False,
        widget=widgets.Input(
            attrs={
                'class': 'form-control',
                'style': 'width: 60%',
            }
        )
    )
    content = forms.CharField(
        label='内容',
        max_length=500,
        required=True,
        widget=widgets.Input(
            attrs={
                'rows': 6,
                'cols': 60,
                'class': 'form-control'
            }
        )
    )

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) <= 10:
            raise forms.ValidationError('内容必须大于10个字')
        return content

    class Meta:
        model = Comments
        fields = ['nickname', 'email', 'website', 'content']


