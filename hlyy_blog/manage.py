#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    # 利用PROJECT_PROFILE环境变量控制settings配置文件是开发还是生成模式
    # 还需修改wsgi.py
    profile = os.environ.get('PROJECT_PROFILE', 'develop')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hlyy_blog.settings.{}'.format(profile))
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
