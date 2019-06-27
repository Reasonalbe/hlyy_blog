# 用作后台管理的Form
from django import forms
from dal import autocomplete

from .models import Category, Tag, Post


class PostAdminForm(forms.ModelForm):
    # 将文章编辑页面的desc字段设置为多行输入框
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='分类',
    )
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        label='标签',
    )
    desc = forms.CharField(widget=forms.Textarea, required=False, label='摘要')
    class Meta:
        model = Post
        fields = ('category', 'tag', 'title', 'desc', 'content', 'status')
        # TODO: 只有在这里放入autocomplete的组件才能有效使用，和静态资源加载顺序有关，记的记录
        widgets = {
            'category': autocomplete.ModelSelect2(url='category-autocomplete'),
            'tag': autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
        }