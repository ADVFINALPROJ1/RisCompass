from rest_framework import serializers

from .models import BusinessSnapshot


class BusinessSnapshotSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    industry_name = serializers.SerializerMethodField(read_only=True)
    region_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BusinessSnapshot
        fields = [
            'id',
            'user',
            'industry',
            'industry_name',
            'region',
            'region_name',
            'title',
            'description',
            'business_stage',
            'startup_budget',
            'currency',
            'target_customer',
            'business_size',
            'has_physical_location',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'industry_name', 'region_name']

    def get_industry_name(self, obj):
        return obj.industry.name if obj.industry else None

    def get_region_name(self, obj):
        return obj.region.region_name if obj.region else None
