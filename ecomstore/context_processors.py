from django.conf import settings

def site_name(request):
    """
    Returns the SITE_NAME from settings as a context variable.
    """
    return {
        'site_name': getattr(settings, 'SITE_NAME', 'Excellent Fashion Wares')
    }