import os

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "podsreunion.settings.development_sqlite")

application = get_wsgi_application()
