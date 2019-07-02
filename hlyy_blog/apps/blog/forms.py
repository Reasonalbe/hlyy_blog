from django import forms
from captcha.fields import CaptchaField

from .models import Comment


class CommentForm(forms.ModelForm):
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})
    email = forms.EmailField(required=False)
    post_id = forms.IntegerField(required=False)

    class Meta:
        model = Comment
        fields = ['nickname', 'content']