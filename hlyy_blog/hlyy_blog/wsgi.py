"""
WSGI config for hlyy_blog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

profile = os.environ.get('HLYY_BLOG_PROFILE', 'develop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hlyy_blog.settings.develop')

application = get_wsgi_application()
