from django.core.mail import EmailMessage
from django.conf import settings
from django.template import loader

from blog.models import Post


def send_email_to_subscriber(email):
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