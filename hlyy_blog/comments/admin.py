from django.contrib import admin

from hlyy_blog.cust_admin_site import custom_site
from .models import Comments
from hlyy_blog.base_admin import BaseOwnerAdmin
# Register your models here.

@admin.register(Comments, site=custom_site)
class CommentsAdmin(BaseOwnerAdmin):
    list_display = ('target', 'nickname', 'website',
                    'email', 'status', 'created_time')
    fields = ('target', 'nickname', 'content', 'website',
                    'email', 'status')