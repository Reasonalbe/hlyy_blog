import xadmin

from .models import Link
from hlyy_blog.admin.base_admin import BaseOwnerAdmin
# Register your models here.


class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'created_time')
    search_fields = ['title']
    fields = ('title', 'href', 'status', 'weight')


xadmin.site.register(Link, LinkAdmin)