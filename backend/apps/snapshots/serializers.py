from rest_framework import serializers

from .models import BusinessSnapshot


class BusinessSnapshotSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = BusinessSnapshot
        fields = [
            'id',
            'user',
            'industry',
            'region',
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
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
