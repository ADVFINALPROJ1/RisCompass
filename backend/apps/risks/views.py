from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.snapshots.models import BusinessSnapshot
from apps.snapshots.permissions import IsOwner
from .models import RiskReport
from .serializers import RiskReportSerializer
from .services.generator import generate_risk_report


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_report(request, snapshot_id):
    """
    Generate a risk report for a specific snapshot.
    
    POST /api/snapshots/<id>/generate-report/
    """
    try:
        snapshot = BusinessSnapshot.objects.get(id=snapshot_id)
    except BusinessSnapshot.DoesNotExist:
        return Response(
            {'detail': 'Snapshot not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check if user owns the snapshot
    if snapshot.user != request.user:
        return Response(
            {'detail': 'You do not have permission to generate a report for this snapshot.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Generate the risk report
    try:
        risk_report = generate_risk_report(snapshot)
        serializer = RiskReportSerializer(risk_report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(
            {'detail': f'Error generating risk report: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_snapshot_reports(request, snapshot_id):
    """
    List all risk reports for a specific snapshot.
    
    GET /api/snapshots/<id>/reports/
    """
    try:
        snapshot = BusinessSnapshot.objects.get(id=snapshot_id)
    except BusinessSnapshot.DoesNotExist:
        return Response(
            {'detail': 'Snapshot not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check if user owns the snapshot
    if snapshot.user != request.user:
        return Response(
            {'detail': 'You do not have permission to view reports for this snapshot.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Get all reports for this snapshot
    reports = RiskReport.objects.filter(snapshot=snapshot)
    serializer = RiskReportSerializer(reports, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_report_detail(request, report_id):
    """
    Get details of a specific risk report.
    
    GET /api/reports/<id>/
    """
    try:
        risk_report = RiskReport.objects.get(id=report_id)
    except RiskReport.DoesNotExist:
        return Response(
            {'detail': 'Risk report not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check if user owns the snapshot associated with this report
    if risk_report.snapshot.user != request.user:
        return Response(
            {'detail': 'You do not have permission to view this report.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = RiskReportSerializer(risk_report)
    return Response(serializer.data, status=status.HTTP_200_OK)
