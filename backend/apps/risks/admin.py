from django.contrib import admin
from .models import RiskReport, RiskFactor


@admin.register(RiskReport)
class RiskReportAdmin(admin.ModelAdmin):
    list_display = ['snapshot', 'overall_risk_score', 'confidence_score', 'created_at']
    list_filter = ['created_at', 'confidence_label']
    search_fields = ['snapshot__title', 'summary']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(RiskFactor)
class RiskFactorAdmin(admin.ModelAdmin):
    list_display = ['report', 'category', 'name', 'score', 'source_type']
    list_filter = ['category', 'source_type', 'created_at']
    search_fields = ['name', 'explanation']
