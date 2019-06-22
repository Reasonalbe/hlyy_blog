# 用作后台管理的Form
from django import forms


class PostAdminForm(forms.ModelForm):
    # 将文章编辑页面的desc字段设置为多行输入框
    desc = forms.CharField(widget=forms.Textarea, required=False, label='摘要')