from django.contrib.admin import AdminSite


class CustomAdminSite(AdminSite):
    site_header = 'HLYY'
    site_title = 'HLYY_Blog管理后台'
    index_title = '首页'

custom_site = CustomAdminSite(name='cust_admin')