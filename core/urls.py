# ecomstore/core/urls.py
from django.urls import path
from . import views

app_name = 'core' # <--- Make sure this app_name is defined for namespacing

urlpatterns = [
    # ... other core URLs if you have any ...
    path('contact/', views.contact_view, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
]