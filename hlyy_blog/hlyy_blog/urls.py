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
import xadmin
from django.urls import path, include
from django.conf import settings
from django.contrib.sitemaps import views as sitemap_views
from django.conf.urls.static import static

from blog.views import PostDetailView, IndexView, CategoryView, TagView, SearchView
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from config.views import LinkView
from comments.views import CommentView
from .autocomplete import CategoryAutocomplete, TagAutocomplete

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('post/<int:post_id>.html', PostDetailView.as_view(), name='post-detail'),
    path('category/<int:category_id>', CategoryView.as_view(), name='category-list'),
    path('tag/<int:tag_id>', TagView.as_view(), name='tag-list'),
    path('search/', SearchView.as_view(), name='search'),
    path('links/', LinkView.as_view(), name='links'),
    path('comment/', CommentView.as_view(), name='comment'),
    path('sitemap.xml', sitemap_views.sitemap, {'sitemaps': {'posts': PostSitemap}}),
    path('rss/', LatestPostFeed(), name='rss'),
    path('xadmin/', xadmin.site.urls, name='xadmin'),
    path('category-autocomplete/', CategoryAutocomplete.as_view(), name='category-autocomplete'),
    path('tag-autocomplete/', TagAutocomplete.as_view(), name='tag-autocomplete'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns