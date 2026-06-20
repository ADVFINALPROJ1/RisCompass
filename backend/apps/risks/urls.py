from django.urls import path

from .views import generate_report, list_snapshot_reports, get_report_detail

urlpatterns = [
    # Generate report for a snapshot
    path('snapshots/<int:snapshot_id>/generate-report/', generate_report, name='generate-report'),
    # List reports for a snapshot
    path('snapshots/<int:snapshot_id>/reports/', list_snapshot_reports, name='list-snapshot-reports'),
    # Get specific report details
    path('reports/<int:report_id>/', get_report_detail, name='report-detail'),
]
