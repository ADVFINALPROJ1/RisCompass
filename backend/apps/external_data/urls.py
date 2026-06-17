from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EconomicIndicatorViewSet, RegionEconomicDataViewSet

router = DefaultRouter()
router.register(r'indicators', EconomicIndicatorViewSet, basename='economicindicator')
router.register(r'data', RegionEconomicDataViewSet, basename='regioneconomicdata')

urlpatterns = [
    path('', include(router.urls)),
]
