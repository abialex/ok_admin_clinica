"""
WSGI config for back_hcl project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from services_external.modules.firebase.utils.firebase_config import Firebase


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "back_hcl.settings")
Firebase.init()
application = get_wsgi_application()
