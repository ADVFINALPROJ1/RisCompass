from django.contrib import admin
from .models import Region


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('region_name', 'country_name', 'country_code', 'region_type', 'is_supported')
    list_filter = ('country_name', 'region_type', 'data_availability_level')
    search_fields = ('region_name', 'country_name', 'city_name', 'country_code')
