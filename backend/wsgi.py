"""
WSGI config for rpc project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os, sys, site

sys.path.insert(0,'/home/ubuntu/dev/proj-be/.venv/lib/python3.9/site-packages')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

#activate_env = "/home/ubuntu/dev/proj-be/.venv/bin/activate"
#exec(open(activate_env).read(), {'__file__': activate_env})

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()