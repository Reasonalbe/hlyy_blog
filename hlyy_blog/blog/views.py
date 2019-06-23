from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Post, Category, Tag
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

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'


class IndexView(ListView, CommonViewMixin):
    template_name = 'index.html'
    queryset = Post.get_latest()
    paginate_by = 1
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