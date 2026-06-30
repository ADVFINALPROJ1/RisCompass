from rest_framework import serializers

from .models import Comparison


class ComparisonSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    snapshot_a_title = serializers.SerializerMethodField(read_only=True)
    snapshot_b_title = serializers.SerializerMethodField(read_only=True)
    winner_snapshot_title = serializers.SerializerMethodField(read_only=True)

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
        ]

    def get_snapshot_a_title(self, obj):
        return obj.snapshot_a.title if obj.snapshot_a else None

    def get_snapshot_b_title(self, obj):
        return obj.snapshot_b.title if obj.snapshot_b else None

    def get_winner_snapshot_title(self, obj):
        return obj.winner_snapshot.title if obj.winner_snapshot else None


class ComparisonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comparison
        fields = [
            'snapshot_a',
            'snapshot_b',
            'title',
            'filter_focus',
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
