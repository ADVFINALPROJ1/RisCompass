from rest_framework import serializers
from .models import Region


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
