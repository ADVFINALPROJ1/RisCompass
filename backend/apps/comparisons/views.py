from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.snapshots.models import BusinessSnapshot
from .models import Comparison
from .serializers import ComparisonSerializer, ComparisonCreateSerializer
from .services.comparison_service import create_comparison


class ComparisonViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing comparisons.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ComparisonSerializer
    
    def get_queryset(self):
        return Comparison.objects.filter(user=self.request.user)
    
    def create(self, request):
        """
        Create a new comparison between two snapshots.
        
        POST /api/comparisons/
        Body: {
            "snapshot_a": <snapshot_id>,
            "snapshot_b": <snapshot_id>,
            "title": <string>,
            "filter_focus": <string>
        }
        """
        serializer = ComparisonCreateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        snapshot_a = serializer.validated_data['snapshot_a']
        snapshot_b = serializer.validated_data['snapshot_b']
        title = serializer.validated_data.get('title')
        filter_focus = serializer.validated_data['filter_focus']
        
        # Security: Users can only compare their own snapshots
        if snapshot_a.user != request.user or snapshot_b.user != request.user:
            return Response(
                {'detail': 'You can only compare your own snapshots.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            comparison = create_comparison(
                user=request.user,
                snapshot_a=snapshot_a,
                snapshot_b=snapshot_b,
                filter_focus=filter_focus
            )
            
            # Override title if provided
            if title:
                comparison.title = title
                comparison.save()
            
            response_serializer = ComparisonSerializer(comparison)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        except ValueError as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'detail': f'Error creating comparison: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def perform_destroy(self, instance):
        # Security check is handled by get_queryset
        instance.delete()
