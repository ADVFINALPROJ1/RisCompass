from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import BusinessSnapshot
from .serializers import BusinessSnapshotSerializer
from .permissions import IsOwner


class BusinessSnapshotViewSet(viewsets.ModelViewSet):
    serializer_class = BusinessSnapshotSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return BusinessSnapshot.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
