from rest_framework import viewsets
from .models import Region
from .serializers import RegionSerializer


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
