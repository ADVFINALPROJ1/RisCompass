from rest_framework import serializers
from .models import Industry, IndustryRiskWeight


class IndustryRiskWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustryRiskWeight
        fields = '__all__'
        read_only_fields = ('id',)


class IndustrySerializer(serializers.ModelSerializer):
    risk_weight = IndustryRiskWeightSerializer(read_only=True)

    class Meta:
        model = Industry
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
