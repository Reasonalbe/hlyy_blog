from .base import *
import os


DEBUG = False

ALLOWED_HOSTS = [
    '127.0.0.1',
    'www.heliyingyou.cn'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hlyy_blog',
        'USER': os.environ.get('DJANGO_MYSQL_USER'),
        'PASSWORD': os.environ.get('DJANGO_MYSQL_PASSWORD'),
        'HOST':'127.0.0.1',
        'PORT':'3306',
        }
    }