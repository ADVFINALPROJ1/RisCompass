from rest_framework import serializers
from .models import EconomicIndicator, RegionEconomicData


class EconomicIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = EconomicIndicator
        fields = [
            'id', 'code', 'name', 'description', 'source',
            'higher_is_riskier', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class RegionEconomicDataSerializer(serializers.ModelSerializer):
    region_name = serializers.CharField(source='region.region_name', read_only=True)
    country_code = serializers.CharField(source='region.country_code', read_only=True)
    country_name = serializers.CharField(source='region.country_name', read_only=True)
    indicator_name = serializers.CharField(source='indicator.name', read_only=True)
    indicator_code = serializers.CharField(source='indicator.code', read_only=True)
    higher_is_riskier = serializers.BooleanField(source='indicator.higher_is_riskier', read_only=True)

    class Meta:
        model = RegionEconomicData
        fields = [
            'id', 'region', 'region_name', 'country_code', 'country_name',
            'indicator', 'indicator_name', 'indicator_code', 'higher_is_riskier',
            'year', 'value', 'source', 'fetched_at', 'is_estimated'
        ]
        read_only_fields = ['fetched_at']


class RegionEconomicDataCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionEconomicData
        fields = [
            'region', 'indicator', 'year', 'value', 'source', 'is_estimated'
        ]
