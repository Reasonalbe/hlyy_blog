from django.contrib import admin

from hlyy_blog.admin.cust_admin_site import custom_site
from .models import Comments
# Register your models here.

@admin.register(Comments, site=custom_site)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('target', 'nickname', 'website',
                    'email', 'status', 'created_time')
    fields = ('target', 'nickname', 'content', 'website',
                    'email', 'status')