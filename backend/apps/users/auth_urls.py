"""
URLs pour l'authentification
"""
from django.urls import path
from . import auth_views

urlpatterns = [
    path('login/', auth_views.login_view, name='auth-login'),
    path('logout/', auth_views.logout_view, name='auth-logout'),
    path('password-reset/', auth_views.password_reset_request, name='password-reset'),
    path('password-reset-confirm/', auth_views.password_reset_confirm, name='password-reset-confirm'),
    path('me/', auth_views.current_user, name='current-user'),
]
