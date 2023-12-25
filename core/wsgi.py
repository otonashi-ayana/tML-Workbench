"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from dtale.app import build_app
from .dispatcher import PathDispatcher

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")


def make_app(prefix):
    if prefix == 'flask':
        return build_app(app_root='/flask', reaper_on=False)


application = PathDispatcher(get_wsgi_application(), make_app)
