from django import forms

from .models import Comment
from util.captcha import jarge_captcha

class FormMixin:
    def get_error(self):
        # 将表单验证的错误信息构造得更可读
        new_errors = {}
        if hasattr(self, 'errors'):
            errors = self.errors.get_json_data()
            for key, message_dicts in errors.items():
                messages = []
                for message in message_dicts:
                    messages.append(message['message'])
                new_errors[key] = messages
        return new_errors

class CommentForm(forms.ModelForm, FormMixin):
    captcha = forms.CharField(max_length=10)
    hashkey = forms.CharField(max_length=100)
    email = forms.EmailField(required=False)
    post_id = forms.IntegerField()
    nickname = forms.CharField(max_length=20, error_messages={
        'max_length': '昵称必须小于20个字符'
    })

    def clean(self):
        # 验证码判断
        capthca = self.cleaned_data.get('captcha')
        hashkey = self.cleaned_data.get('hashkey')
        if not jarge_captcha(capthca, hashkey):
            raise forms.ValidationError('验证码错误')

    class Meta:
        model = Comment
        fields = ['nickname', 'content']