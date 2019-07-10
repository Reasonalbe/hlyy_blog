import xadmin
from django.db.models import Count
from xadmin.layout import Fieldset
from xadmin.filters import manager, RelatedFieldListFilter

from .adminforms import PostAdminForm
from .models import Tag, Post
from hlyy_blog.admin.base_admin import BaseOwnerAdmin
# Register your models here.


class TagContainFilter(RelatedFieldListFilter):
    """自定义过滤器,展示每个分类下有几篇文章"""
    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'tag'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        id_name_count = Tag.objects.filter(owner=request.user). \
            annotate(post_count=Count('post')).only('id', 'name').order_by('name')
        self.lookup_choices = [(qs.id, '{}（{}）'.format(qs.name, qs.post_count)) for qs in id_name_count]

manager.register(TagContainFilter, take_priority=True)


class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'post_count', 'created_time')
    fields = ('name', 'status', 'is_nav' )
    search_fields = ['name', 'id', ]
    def get_list_queryset(self):
        qs = super().get_list_queryset()
        return qs.annotate(post_count=Count('post'))

    def post_count(self, obj):
        return obj.post_count
    post_count.short_description = '文章数量'

class PostAdmin(BaseOwnerAdmin):
    list_display = ('title', 'status', 'tag','created_time', 'send_subscriber')
    list_filter = [
       'tag',
    ]
    # 外键的字段通过双下划线访问
    search_fields = ['title', ]
    actions_on_top = True
    actions_on_bottom = True
    save_on_top = True
    form = PostAdminForm
    form_layout = (
        Fieldset(
            '基础信息',
            'title',
            'status',
            'tag',
            'send_subscriber',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'content'
        )
    )

    #自定义展示列
    def my_tag(self, obj):
        return obj.tags
    my_tag.short_description = '标签'

    def save_models(self):
        pass


xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(Post, PostAdmin)