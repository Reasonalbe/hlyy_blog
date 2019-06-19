from .base import * # NOQA

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hlyy_blog',
        'USER':'root',
        'PASSWORD':'heli19950610',
        'HOST':'127.0.0.1',
        'PORT':'3306',
        }
    }