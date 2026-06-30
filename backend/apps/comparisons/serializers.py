from rest_framework import serializers

from .models import Comparison


class ComparisonSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    snapshot_a_title = serializers.SerializerMethodField(read_only=True)
    snapshot_b_title = serializers.SerializerMethodField(read_only=True)
    winner_snapshot_title = serializers.SerializerMethodField(read_only=True)
    snapshot_a_score = serializers.SerializerMethodField(read_only=True)
    snapshot_b_score = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comparison
        fields = [
            'id',
            'user',
            'snapshot_a',
            'snapshot_a_title',
            'snapshot_b',
            'snapshot_b_title',
            'title',
            'filter_focus',
            'winner_snapshot',
            'winner_snapshot_title',
            'summary',
            'snapshot_a_score',
            'snapshot_b_score',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'user',
            'created_at',
            'updated_at',
            'snapshot_a_title',
            'snapshot_b_title',
            'winner_snapshot_title',
            'winner_snapshot',
            'summary',
            'snapshot_a_score',
            'snapshot_b_score',
        ]

    def get_snapshot_a_title(self, obj):
        return obj.snapshot_a.title if obj.snapshot_a else None

    def get_snapshot_b_title(self, obj):
        return obj.snapshot_b.title if obj.snapshot_b else None

    def get_winner_snapshot_title(self, obj):
        return obj.winner_snapshot.title if obj.winner_snapshot else None

    def get_snapshot_a_score(self, obj):
        try:
            from apps.risks.models import RiskReport
            report = RiskReport.objects.filter(snapshot=obj.snapshot_a).latest('created_at')
            score_field_map = {
                Comparison.FILTER_FOCUS_OVERALL: 'overall_risk_score',
                Comparison.FILTER_FOCUS_FINANCIAL: 'financial_risk',
                Comparison.FILTER_FOCUS_MARKET: 'market_risk',
                Comparison.FILTER_FOCUS_LEGAL: 'legal_risk',
                Comparison.FILTER_FOCUS_CULTURAL: 'cultural_risk',
                Comparison.FILTER_FOCUS_OPERATIONAL: 'operational_risk',
            }
            score_field = score_field_map.get(obj.filter_focus, 'overall_risk_score')
            return getattr(report, score_field)
        except Exception:
            return None

    def get_snapshot_b_score(self, obj):
        try:
            from apps.risks.models import RiskReport
            report = RiskReport.objects.filter(snapshot=obj.snapshot_b).latest('created_at')
            score_field_map = {
                Comparison.FILTER_FOCUS_OVERALL: 'overall_risk_score',
                Comparison.FILTER_FOCUS_FINANCIAL: 'financial_risk',
                Comparison.FILTER_FOCUS_MARKET: 'market_risk',
                Comparison.FILTER_FOCUS_LEGAL: 'legal_risk',
                Comparison.FILTER_FOCUS_CULTURAL: 'cultural_risk',
                Comparison.FILTER_FOCUS_OPERATIONAL: 'operational_risk',
            }
            score_field = score_field_map.get(obj.filter_focus, 'overall_risk_score')
            return getattr(report, score_field)
        except Exception:
            return None


class ComparisonCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = Comparison
        fields = [
            'snapshot_a',
            'snapshot_b',
            'filter_focus',
            'title',
        ]

    def validate(self, attrs):
        snapshot_a = attrs.get('snapshot_a')
        snapshot_b = attrs.get('snapshot_b')
        
        # Ensure snapshots are different
        if snapshot_a == snapshot_b:
            raise serializers.ValidationError(
                "Snapshot A and Snapshot B must be different."
            )
        
        return attrs
