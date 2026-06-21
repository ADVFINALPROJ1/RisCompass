from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import BusinessSnapshotViewSet

router = DefaultRouter()
router.register(r'', BusinessSnapshotViewSet, basename='businesssnapshot')

urlpatterns = [
    path('', include(router.urls)),
]
