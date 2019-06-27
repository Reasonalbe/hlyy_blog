import xadmin
from django.utils.html import format_html
from django.shortcuts import reverse
from django.db.models import Count
from xadmin.layout import Row, Fieldset
from xadmin.filters import manager, RelatedFieldListFilter

from .adminforms import PostAdminForm
from .models import Tag, Post, Category
from hlyy_blog.admin.base_admin import BaseOwnerAdmin
# Register your models here.


class CategoryOwnerFilter(RelatedFieldListFilter):
    """自定义过滤器只展示当前用户分类"""
    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        id_name_count = Category.objects.filter(owner=request.user). \
            annotate(post_count=Count('post')).only('id', 'name').order_by('name')
        self.lookup_choices = [(qs.id, '{}（{}）'.format(qs.name, qs.post_count)) for qs in id_name_count]

manager.register(CategoryOwnerFilter, take_priority=True)


class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'post_count', 'created_time')
    search_fields = ['name', 'id']
    # 在admin中管理的字段
    fields = ('name', 'status', 'is_nav')
    # 展示每个分类所包含文章数列表
    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'


class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')
    search_fields = ['name', 'id']

class PostAdmin(BaseOwnerAdmin):
    list_display = ('title', 'status', 'category', 'created_time', 'operator')
    list_display_links = []
    list_filter = [
       'category',
    ]
    # 外键的字段通过双下划线访问
    search_fields = ['title', 'category__name']
    actions_on_top = True
    actions_on_bottom = True
    save_on_top = True
    form = PostAdminForm
    autocomplete_fields = ['category', 'tag']
    form_layout = (
        Fieldset(
            '基础信息',
            Row('title', 'category'),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'content'
        )
    )

    #自定义展示列
    def operator(self, obj):
        return format_html('<a href="{}">编辑</a>',
                           reverse('xadmin:blog_post_change', args=(obj.id,)))
    operator.short_description = '操作'


xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(Post, PostAdmin)