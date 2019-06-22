from django.contrib import admin

from .models import Link, SideBar
from hlyy_blog.cust_admin_site import custom_site
from hlyy_blog.base_admin import BaseOwnerAdmin
# Register your models here.


@admin.register(Link, site=custom_site)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'created_time')
    search_fields = ['title']
    fields = ('title', 'href', 'status', 'weight')

@admin.register(SideBar, site=custom_site)
class SideBarAdmin(BaseOwnerAdmin):
    list_display = ('title', 'display_type', 'status', 'created_time')
    fields = ('title', 'display_type', 'content', 'status')