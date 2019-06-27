import xadmin
from django.contrib import admin

from .models import Comments
# Register your models here.

class CommentsAdmin:
    list_display = ('target', 'nickname', 'website',
                    'email', 'status', 'created_time')
    fields = ('target', 'nickname', 'content', 'website',
                    'email', 'status')

xadmin.site.register(Comments, CommentsAdmin)