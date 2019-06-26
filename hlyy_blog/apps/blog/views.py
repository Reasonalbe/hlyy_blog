from datetime import date

from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView
from django.db.models import Q, F
from django.core.cache import cache

from .models import Post, Category, Tag
from comments.models import Comments
from comments.forms import CommentForm
from config.models import SideBar


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        """获取侧边栏、导航分类栏以及底部分类栏的数据"""
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars':SideBar.get_all()
        })
        context.update(Category.get_navs())
        return context

class PostDetailView(CommonViewMixin, DetailView):
    # Mixin父类需放在前面
    # TODO: 复习继承顺序
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'comment_list': Comments.get_by_target(self.request.path),
            'comment_form': CommentForm()
        })
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        """处理访问统计，根据缓存中的UID判断是否增加PV与UV"""
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:{}:{}'.format(uid, self.request.path)
        uv_key = 'uv:{}:{}:{}'.format(uid, self.request.path, str(date.today()))
        if not cache.get(pv_key):
            increase_pv = True
            # PV缓存1分钟防止刷访问量
            cache.set(pv_key, 1, 1*60)
        if not cache.get(uv_key):
            increase_uv = True
            # UV缓存设置1天
            cache.set(uv_key, 1, 60*60*24)

        if increase_uv and increase_pv:
            # 能一次更新的操作就不要分两次做
            # DetailView类的实例包含object属性，指向当前view中获取的model实例
            Post.objects.filter(pk=self.object.id)\
                .update(pv=F('pv') + 1, uv=F('uv') + 1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id) \
                .update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id) \
                .update(uv=F('uv') + 1)

class IndexView(CommonViewMixin, ListView):
    template_name = 'index.html'
    queryset = Post.get_latest()
    paginate_by = 10
    context_object_name = 'post_list'# 设置模板中使用的变量名

class CategoryView(IndexView):
    def get_context_data(self, *, object_list=None, **kwargs):
        """在上下文中增加选中的分类的数据"""
        context_data = super().get_context_data(object_list=object_list, **kwargs)
        # self.kwargs为URL传递的参数
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context_data.update({
            'category': category
        })
        return context_data

    def get_queryset(self):
        """根据分类过滤文章"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        queryset = queryset.filter(category__id=category_id)
        return queryset

class TagView(IndexView):
    def get_context_data(self, *, object_list=None, **kwargs):
        """在上下文中增加选中的标签的数据"""
        context_data = super().get_context_data(object_list=object_list, **kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Category, pk=tag_id)
        context_data.update({
            'tag': tag
        })
        return context_data

    def get_queryset(self):
        """根据标签过滤文章"""
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        queryset = queryset.filter(tag__id=tag_id)
        return queryset

class SearchView(IndexView):
    def get_queryset(self):
        qs = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return qs
        else:
            return qs.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context