from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.regions.models import Region
from .models import EconomicIndicator, RegionEconomicData
from .serializers import (
    EconomicIndicatorSerializer,
    RegionEconomicDataSerializer,
    RegionEconomicDataCreateSerializer
)
from .services.world_bank import fetch_world_bank_indicator
from .normalizers import (
    normalize_inflation_to_risk,
    normalize_unemployment_to_risk,
    normalize_internet_usage_to_risk,
    normalize_gdp_growth_to_risk
)


class EconomicIndicatorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing EconomicIndicator records.
    """
    queryset = EconomicIndicator.objects.all()
    serializer_class = EconomicIndicatorSerializer
    lookup_field = 'code'

    def get_queryset(self):
        queryset = super().get_queryset()
        code = self.request.query_params.get('code')
        if code:
            queryset = queryset.filter(code__icontains=code)
        return queryset


class RegionEconomicDataViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing RegionEconomicData records.
    """
    queryset = RegionEconomicData.objects.select_related('region', 'indicator').all()
    serializer_class = RegionEconomicDataSerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RegionEconomicDataCreateSerializer
        return RegionEconomicDataSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        region_id = self.request.query_params.get('region')
        indicator_code = self.request.query_params.get('indicator')
        year = self.request.query_params.get('year')
        country_code = self.request.query_params.get('country_code')

        if region_id:
            queryset = queryset.filter(region_id=region_id)
        if indicator_code:
            queryset = queryset.filter(indicator__code=indicator_code)
        if year:
            queryset = queryset.filter(year=year)
        if country_code:
            queryset = queryset.filter(region__country_code=country_code)

        return queryset

    @action(detail=False, methods=['get'])
    def by_region(self, request):
        """
        Get all economic data for a specific region.
        """
        region_id = request.query_params.get('region_id')
        if not region_id:
            return Response(
                {'error': 'region_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = self.get_queryset().filter(region_id=region_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def latest(self, request):
        """
        Get the latest economic data for a region and indicator.
        """
        region_id = request.query_params.get('region_id')
        indicator_code = request.query_params.get('indicator_code')

        if not region_id or not indicator_code:
            return Response(
                {'error': 'region_id and indicator_code parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            latest_data = self.get_queryset().filter(
                region_id=region_id,
                indicator__code=indicator_code
            ).order_by('-year').first()

            if not latest_data:
                return Response(
                    {'error': 'No data found for this region and indicator'},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = self.get_serializer(latest_data)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def fetch_from_world_bank(self, request):
        """
        Fetch economic data from World Bank API and store it.
        """
        country_code = request.data.get('country_code')
        indicator_code = request.data.get('indicator_code')

        if not country_code or not indicator_code:
            return Response(
                {'error': 'country_code and indicator_code are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch data from World Bank API
        data = fetch_world_bank_indicator(country_code, indicator_code)

        if not data:
            return Response(
                {'error': 'Failed to fetch data from World Bank API'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            # Get or create indicator
            indicator = get_object_or_404(
                EconomicIndicator,
                code=indicator_code
            )

            # Find region by country code
            region = Region.objects.filter(country_code=country_code).first()
            if not region:
                return Response(
                    {'error': f'No region found with country code: {country_code}'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Create or update RegionEconomicData
            economic_data, created = RegionEconomicData.objects.update_or_create(
                region=region,
                indicator=indicator,
                year=int(data['year']),
                defaults={
                    'value': data['value'],
                    'source': data['source'],
                    'is_estimated': False
                }
            )

            serializer = RegionEconomicDataSerializer(economic_data)
            return Response(
                {
                    'data': serializer.data,
                    'created': created
                },
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def calculate_risk(self, request):
        """
        Calculate risk score for a specific indicator value.
        """
        indicator_code = request.query_params.get('indicator_code')
        value = request.query_params.get('value')

        if not indicator_code or value is None:
            return Response(
                {'error': 'indicator_code and value parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            value = float(value)
        except (ValueError, TypeError):
            return Response(
                {'error': 'value must be a number'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Map indicator codes to normalizer functions
        normalizer_map = {
            'FP.CPI.TOTL.ZG': normalize_inflation_to_risk,
            'SL.UEM.TOTL.ZS': normalize_unemployment_to_risk,
            'IT.NET.USER.ZS': normalize_internet_usage_to_risk,
            'NY.GDP.MKTP.KD.ZG': normalize_gdp_growth_to_risk,
        }

        normalizer = normalizer_map.get(indicator_code)
        if not normalizer:
            return Response(
                {'error': f'No normalizer available for indicator: {indicator_code}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        risk_score = normalizer(value)
        return Response({
            'indicator_code': indicator_code,
            'value': value,
            'risk_score': risk_score
        })
