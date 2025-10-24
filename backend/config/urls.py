"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Health Check & Monitoring
    path('monitoring/', lambda request: __import__('django.shortcuts').shortcuts.render(request, 'monitoring_dashboard.html'), name='monitoring-dashboard'),
    path('api/health/', include([
        path('', lambda r: __import__('apps.monitoring').monitoring.HealthCheckView.as_view()(r), name='health-check'),
        path('quick/', lambda r: __import__('apps.monitoring').monitoring.QuickHealthView.as_view()(r), name='health-quick'),
        path('stats/', lambda r: __import__('apps.monitoring').monitoring.DetailedStatsView.as_view()(r), name='health-stats'),
    ])),
    
    # API Routes
    path('api/auth/', include('apps.users.auth_urls')),  # Authentication routes
    path('api/', include('apps.users.urls')),  # /users, /teams, /users/{id}/clocks
    path('api/attendance/', include('apps.attendance.urls')),  # /attendance/*, /clocks, /reports
]

# Django Debug Toolbar (development only)
if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
