from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import reverse
from django.db.models import Count
from django.contrib.admin.models import LogEntry

from .adminforms import PostAdminForm
from .models import Tag, Post, Category
from hlyy_blog.cust_admin_site import custom_site
from hlyy_blog.base_admin import BaseOwnerAdmin
# Register your models here.


# class PostInline(admin.TabularInline):
#     fields = ('title', 'desc')
#     extra = 1
#     model = Post

class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户分类"""

    title = '分类过滤器'
    # URL查询参数名字
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        # 必须重写此函数，返回一个二维元祖（url的参数, 显示内容）的列表
        id_name_count = Category.objects.filter(owner=request.user).\
            annotate(post_count=Count('post')).only('id', 'name').order_by('name')
        return [(qs.id, '{}（{}）'.format(qs.name, qs.post_count)) for qs in id_name_count]


    def queryset(self, request, queryset):
        # self.value()是url的查询参数的值，此处就是owner_category
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset

@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'post_count', 'created_time')
    # 在admin中管理的字段
    fields = ('name', 'status', 'is_nav')
    # inlines = [PostInline, ]
    # 展示每个分类所包含文章数列表
    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    list_display = ('title', 'status', 'category', 'created_time', 'operator')
    list_display_links = []
    list_filter = [
        CategoryOwnerFilter,
    ]
    # 外键的字段通过双下划线访问
    search_fields = ['title', 'category__name']
    actions_on_top = True
    actions_on_bottom = True
    save_on_top = True
    form = PostAdminForm

    fieldsets = (
        ('基础配置', {
            'fields': (
                ('title', 'category'),
                'status'
            )
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            )
        }),
        ('额外信息', {
            'description': '标签',
            'classes': ('collapse',),
            'fields': ('tag',)
        })
    )

    #自定义展示列
    def operator(self, obj):
        return format_html('<a href="{}">编辑</a>',
                           reverse('cust_admin:blog_post_change', args=(obj.id,)))
    operator.short_description = '操作'

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user',
                    'action_time', 'change_message']