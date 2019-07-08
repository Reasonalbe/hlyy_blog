from django.conf import settings
from django.core.mail import EmailMessage
from django.template import loader
from django.views.generic import ListView, View

from blog.models import Post
from blog.views import CommonViewMixin
from util import restful
from .forms import SubscribeForm
from .models import Link, Subscribe


class LinkView(ListView, CommonViewMixin):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'config/links.html'

class SubscribeView(View):
    def post(self, request):
        subscribe_form = SubscribeForm(request.POST)
        message = ''
        if subscribe_form.is_valid():
            email = subscribe_form.cleaned_data.get('email')
            try:
                subscribe = Subscribe.objects.get(email=email)
            except Subscribe.DoesNotExist:
                subscribe_form.save()
                message = '感谢您的订阅！'
            else:
                # 若已经订阅则切换订阅者的状态
                if subscribe.status == Subscribe.STATUS_NORMAL:
                    subscribe.status = Subscribe.STATUS_DELETE
                    message = '您已取消了订阅！'
                else:
                    subscribe.status = Subscribe.STATUS_NORMAL
                    message = '感谢您的再次订阅'
                subscribe.save()
            return restful.result(message=message)
        else:
            return restful.paramserror(subscribe_form.get_error())

    def get(self, request):
        """get请求直接将所有尚未发送给订阅者的文章发送给所有订阅者"""
        # 判断是否还有未发送给订阅者的文章
        has_unsended_posts = Post.objects.filter(send_subscriber=False).exists()
        if has_unsended_posts:
            # 找到所有订阅者的邮箱
            emails = [subscribe.email for subscribe in Subscribe.objects.only('email')]
            try:
                # 发送邮件
                self.send_email_to_subscriber(emails)
            except Exception:
                # 失败返回错误信息
                return restful.servererror('邮件发送失败')
            else:
                # 成功后将所有文章的send_subscriber字段改为True
                Post.objects.filter(send_subscriber=False).update(send_subscriber=True)
                return restful.ok()
        else:
            return restful.servererror(message='没有还未发送给订阅者的文章')


    def send_email_to_subscriber(self, email):
        """将所有未发送给订阅者的文章通过邮件发送给订阅者"""
        email = list(email)
        email_title = "HLYY Blog更新内容啦！"
        email_body = loader.render_to_string(
            'config/to_subscriber.html',
            {
                'posts': Post.get_unsent_to_subscriber_post()
            }
        )
        msg = EmailMessage(email_title, email_body, settings.EMAIL_FROM, email)
        msg.content_subtype = "html"
        send_status = msg.send()
        return send_status