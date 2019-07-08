from django.template import loader
from xadmin.views import BaseAdminPlugin, ListAdminView
from xadmin.sites import site

from .models import Link, Subscribe
from hlyy_blog.admin.base_admin import BaseOwnerAdmin
# Register your models here.


class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'created_time')
    search_fields = ['title']
    fields = ('title', 'href', 'status', 'weight')

class SubscribeAdmin():
    list_display = ('email', 'status', 'created_time')
    fields = ('email', 'status',)

    # @property
    # def media(self):
    #     media = super(SubscribeAdmin, self).media
    #     media += [self.static('js/my_ajax.js'),
    #                   self.static('js/my_alert.js'),
    #                   self.static('js/sweetalert.min.js'),
    #                   self.static('js/subscribe.js'),
    #                   ]
    #     return media

class SubscribePlugin(BaseAdminPlugin):
    """发送订阅的插件"""
    def init_request(self, *args, **kwargs):
        """初始化插件，返回bool，代表是否启用该插件"""
        # 确保只有在订阅模型的adminview中启动该插件
        if self.model == Subscribe:
            return True
        return False

    def block_nav_btns(self, context, nodes):
        """在页面中toolbar增加发送邮件按钮"""
        nodes.append(loader.render_to_string('config/xadmin_plugin_subscribe_button.html'))

    # def get_media(self, media):
    #     # 拦截了adminview的get_media方法，加入了自定义js用于提醒发送邮件成功
    #     # media = super().get_media() + self.vendor('xadmin.page.list.js', 'xadmin.page.form.js')
    #     media.add_js()
    #     return media

site.register(Link, LinkAdmin)
site.register(Subscribe, SubscribeAdmin)
# TODO: plugin只能注册到xadmin自带的AdminView中，不能注册到自己的View中
site.register_plugin(SubscribePlugin, ListAdminView)