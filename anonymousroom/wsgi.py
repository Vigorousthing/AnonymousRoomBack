"""
WSGI config for anonymousroom project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anonymousroom.settings')

application = get_wsgi_application()


# import os
#
# from django.core.wsgi import get_wsgi_application
#
# if os.environ.get('DEV') is True:
#    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "anonymousroom.settings.dev")
# else:
#    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
#    "anonymousroom.settings.production")
#
# application = get_wsgi_application()