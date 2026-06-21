from rest_framework import serializers

from .models import RiskReport, RiskFactor


class RiskFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskFactor
        fields = [
            'id',
            'category',
            'name',
            'score',
            'explanation',
            'source_type',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class RiskReportSerializer(serializers.ModelSerializer):
    risk_factors = RiskFactorSerializer(many=True, read_only=True)
    snapshot_title = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RiskReport
        fields = [
            'id',
            'snapshot',
            'snapshot_title',
            'overall_risk_score',
            'confidence_score',
            'confidence_label',
            'financial_risk',
            'market_risk',
            'legal_risk',
            'cultural_risk',
            'operational_risk',
            'summary',
            'recommendation',
            'data_sources_used',
            'risk_factors',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'risk_factors',
            'snapshot_title',
        ]

    def get_snapshot_title(self, obj):
        return obj.snapshot.title if obj.snapshot else None
