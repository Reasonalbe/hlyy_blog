from django import forms

from .models import Comment
from util.captcha import jarge_captcha


class CommentForm(forms.ModelForm):
    captcha = forms.CharField(max_length=10)
    hashkey = forms.CharField(max_length=100)
    email = forms.EmailField(required=False)
    post_id = forms.IntegerField()

    def clean(self):
        capthca = self.cleaned_data.get('captcha')
        hashkey = self.cleaned_data.get('hashkey')
        if not jarge_captcha(capthca, hashkey):
            raise forms.ValidationError('验证码错误')

    class Meta:
        model = Comment
        fields = ['nickname', 'content']