# 用作后台管理的Form
from django import forms
from dal import autocomplete
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Tag, Post


class PostAdminForm(forms.ModelForm):
    # 将文章编辑页面的desc字段设置为多行输入框并将正文输入改为富文本编辑器
    # 并未tga字段添加了autocomplete组件
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        label='标签',
    )
    desc = forms.CharField(widget=forms.Textarea, required=False, label='摘要')
    content = forms.CharField(widget=CKEditorUploadingWidget(), label='正文', required=True)
    class Meta:
        model = Post
        fields = ('tag', 'title', 'desc', 'content', 'status')
        # TODO: 只有在这里放入autocomplete的组件才能有效使用，和静态资源加载顺序有关，记的记录
        widgets = {
            'tag': autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
        }