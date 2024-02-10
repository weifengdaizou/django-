"""
WSGI config for bokexit project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bokexit.settings")

application = get_wsgi_application()

r


@receiver(session_deleted)
def session_expired_callback(sender, **kwargs):
    # 在这里添加您的函数逻辑，例如调用某个清理函数或执行其他操作
    pass



