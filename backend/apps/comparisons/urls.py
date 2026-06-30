from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ComparisonViewSet

router = DefaultRouter()
router.register(r'', ComparisonViewSet, basename='comparison')

urlpatterns = [
    path('', include(router.urls)),
]
