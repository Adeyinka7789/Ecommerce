# your_app/context_processors.py
from django.conf import settings

def site_settings(request):
    return {'site_name': settings.SITE_NAME}