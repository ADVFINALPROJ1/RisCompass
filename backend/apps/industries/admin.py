from django.contrib import admin
from .models import Industry, IndustryRiskWeight


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name', 'default_risk_level')
    search_fields = ('name',)


@admin.register(IndustryRiskWeight)
class IndustryRiskWeightAdmin(admin.ModelAdmin):
    list_display = ('industry', 'financial_weight', 'market_weight', 'legal_weight', 'cultural_weight', 'operational_weight')
