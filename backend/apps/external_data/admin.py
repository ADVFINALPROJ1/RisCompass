from django.contrib import admin
from .models import EconomicIndicator, RegionEconomicData


@admin.register(EconomicIndicator)
class EconomicIndicatorAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'source', 'higher_is_riskier', 'created_at', 'updated_at']
    list_filter = ['higher_is_riskier', 'source']
    search_fields = ['code', 'name', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(RegionEconomicData)
class RegionEconomicDataAdmin(admin.ModelAdmin):
    list_display = ['region', 'indicator', 'year', 'value', 'source', 'is_estimated', 'fetched_at']
    list_filter = ['indicator', 'year', 'is_estimated', 'source']
    search_fields = ['region__country_name', 'region__region_name', 'indicator__code']
    readonly_fields = ['fetched_at']
