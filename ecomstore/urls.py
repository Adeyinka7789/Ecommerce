# ecomstore/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
# REMOVE THIS LINE: from products.views import home_page_view
# Import settings and static for serving media files *only in development*
from django.conf import settings
from django.conf.urls.static import static

# Import Django's built-in LoginView and LogoutView
from django.contrib.auth import views as auth_views # <-- ADD THIS LINE

from .views import (SignUpView,
                    profile_view,
                    order_history_view,
                    order_detail_view,
                    profile_edit_view,
                    address_edit_view,
                    address_list_view,
                    address_delete_view,)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('preview.urls')), # This will now be your primary homepage
    path('cart/', include('cart.urls', namespace='cart')),
    # REMOVE THIS LINE: path('home/', home_page_view, name='home'), # Home page view
    path('products/', include('products.urls', namespace='products')),
    path('checkout/', include('checkout.urls', namespace='checkout')),

    # COMMENT OUT OR REMOVE THIS LINE:
    # path('accounts/', include('django.contrib.auth.urls')),

    # ADD THESE EXPLICIT AUTHENTICATION URLS:
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html',
            extra_context={'site_name': settings.SITE_NAME} # <-- This passes the site_name
        ),
        name='login'
    ),
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL),
        name='logout'
    ),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),


    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/profile/', profile_view, name='profile'),
    path('accounts/orders/', order_history_view, name='order_history'),
    path('accounts/orders/<int:order_id>/', order_detail_view, name='order_detail'),
    path('accounts/profile/edit/', profile_edit_view, name='profile_edit'),

    # NEW: User Address Management URLs
    path('accounts/addresses/', address_list_view, name='address_list'),
    path('accounts/addresses/add/', address_edit_view, name='address_add'),
    path('accounts/addresses/edit/<int:address_id>/', address_edit_view, name='address_edit'),
    path('accounts/addresses/delete/<int:address_id>/', address_delete_view, name='address_delete'),

    # NEW: Wishlist URLs
    path('accounts/wishlist/', include('wishlist.urls')),

    path('', include('core.urls')), # Contact form URL

    path('analytics/', include('analytics.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)