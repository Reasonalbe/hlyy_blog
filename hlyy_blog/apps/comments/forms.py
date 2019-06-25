import mistune
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
        # TODO:将form的validation操作顺序写在博客上
        # clean_<field>方法将在field的clean()方法之后调用，
        # 不接受参数，从self.cleaned_data中获取数据
        # 返回只将覆盖cleaned_data中的数据
        # 该函数在form.clean()方法之前
        content = self.cleaned_data.get('content')
        if len(content) <= 10:
            raise forms.ValidationError('内容必须大于10个字')
        # 转化为markdown格式的HTML
        content = mistune.markdown(content)
        return content

    class Meta:
        model = Comments
        fields = ['nickname', 'email', 'website', 'content']


