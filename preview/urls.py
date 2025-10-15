from django.urls import path
from . import views # Import your views from the same app

urlpatterns = [
    path('', views.home, name='home'), # Map the root URL of this app to your home view
    path('about/', views.about, name='about'), # Map the about URL to your about view
]