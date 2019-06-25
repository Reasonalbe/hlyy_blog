from django.shortcuts import render
from django.views.generic import ListView

from .models import Link
from blog.views import CommonViewMixin


class LinkView(ListView, CommonViewMixin):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'config/links.html'
