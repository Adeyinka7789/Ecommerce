# products/urls.py
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name='product_list'),  # Changed to index view
    path('products/', views.product_list, name='product_list_all'),  # New path for product_list
    path('search/', views.search_products, name='search_products'),
    path('category/<slug:category_slug>/', views.product_list, name='category_detail'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]