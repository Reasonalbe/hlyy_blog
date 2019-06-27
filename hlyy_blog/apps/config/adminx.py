import xadmin

from .models import Link, SideBar
from hlyy_blog.admin.base_admin import BaseOwnerAdmin
# Register your models here.


class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'created_time')
    search_fields = ['title']
    fields = ('title', 'href', 'status', 'weight')

class SideBarAdmin(BaseOwnerAdmin):
    list_display = ('title', 'display_type', 'status', 'created_time')
    fields = ('title', 'display_type', 'content', 'status')

xadmin.site.register(Link, LinkAdmin)
xadmin.site.register(SideBar, SideBarAdmin)