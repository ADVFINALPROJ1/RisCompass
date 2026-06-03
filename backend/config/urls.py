"""
URL Configuration for RisCompass Django Backend

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # JWT Token endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API v1 routes
    # path('api/v1/risks/', include('apps.risks.urls')),
    # path('api/v1/reports/', include('apps.reports.urls')),
    # path('api/v1/users/', include('apps.users.urls')),
    
    # Health check (optional)
    # path('api/health/', views.health_check, name='health_check'),
]
