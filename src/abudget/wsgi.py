import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "abudget.settings.base")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
