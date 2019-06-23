"""hlyy_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from hlyy_blog.cust_admin_site import custom_site
from blog.views import PostDetailView, IndexView, CategoryView, TagView

urlpatterns = [
    # 将用户管理与业务内容管理分成两个网站
    # 实际上是基于一套管理系统，只是在url上进行区分
    path('super_admin/', admin.site.urls),
    path('admin/', custom_site.urls),
    path('/', IndexView.as_view(), name='index'),
    path('post/<int:post_id>.html', PostDetailView.as_view(), name='post-detail'),
    path('category/<int:category_id>', CategoryView.as_view(), name='category-lst'),
    path('tag/<int:tag_id>', TagView.as_view(), name='tag-lst'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns