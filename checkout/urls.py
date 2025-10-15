# checkout/urls.py

from django.urls import path
from . import views

app_name = 'checkout' # Namespace for checkout URLs

urlpatterns = [
    path('', views.checkout_page, name='checkout_page'),
    path('create-paystack-payment/', views.create_paystack_payment, name='create_paystack_payment'),
    path('success/', views.checkout_success, name='checkout_success'),
    path('cancel/', views.checkout_cancel, name='checkout_cancel'),
    path('confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]