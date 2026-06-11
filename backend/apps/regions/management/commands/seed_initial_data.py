from django.core.management.base import BaseCommand
from decimal import Decimal


class Command(BaseCommand):
    help = 'Seed initial regions and industries data for RisCompass'

    def handle(self, *args, **options):
        from apps.regions.models import Region
        from apps.industries.models import Industry, IndustryRiskWeight

        regions = [
            {
                'region_name': 'Berlin',
                'country_name': 'Germany',
                'country_code': 'DEU',
                'city_name': 'Berlin',
                'region_type': 'urban',
                'data_availability_level': 'high',
                'is_supported': True,
            },
            {
                'region_name': 'London',
                'country_name': 'United Kingdom',
                'country_code': 'GBR',
                'city_name': 'London',
                'region_type': 'urban',
                'data_availability_level': 'high',
                'is_supported': True,
            },
            {
                'region_name': 'Addis Ababa',
                'country_name': 'Ethiopia',
                'country_code': 'ETH',
                'city_name': 'Addis Ababa',
                'region_type': 'urban',
                'data_availability_level': 'medium',
                'is_supported': False,
            },
            {
                'region_name': 'Nairobi',
                'country_name': 'Kenya',
                'country_code': 'KEN',
                'city_name': 'Nairobi',
                'region_type': 'urban',
                'data_availability_level': 'medium',
                'is_supported': False,
            },
            {
                'region_name': 'Remote Ethiopia Region',
                'country_name': 'Ethiopia',
                'country_code': 'ETH',
                'city_name': '',
                'region_type': 'remote',
                'data_availability_level': 'low',
                'is_supported': False,
            },
            {
                'region_name': 'Lagos',
                'country_name': 'Nigeria',
                'country_code': 'NGA',
                'city_name': 'Lagos',
                'region_type': 'urban',
                'data_availability_level': 'medium',
                'is_supported': False,
            },
        ]

        for r in regions:
            obj, created = Region.objects.update_or_create(
                country_code=r['country_code'],
                region_name=r['region_name'],
                defaults={
                    'country_name': r['country_name'],
                    'city_name': r['city_name'],
                    'region_type': r['region_type'],
                    'data_availability_level': r['data_availability_level'],
                    'is_supported': r['is_supported'],
                }
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(f"{action} region: {obj}")

        # Industries and weights
        industries = [
            {
                'name': 'Retail',
                'description': 'Retail industry',
                'default_risk_level': 'medium',
                'weights': {
                    'financial_weight': Decimal('0.30'),
                    'market_weight': Decimal('0.25'),
                    'legal_weight': Decimal('0.15'),
                    'cultural_weight': Decimal('0.15'),
                    'operational_weight': Decimal('0.15'),
                }
            },
            {
                'name': 'Tech',
                'description': 'Technology industry',
                'default_risk_level': 'high',
                'weights': {
                    'financial_weight': Decimal('0.20'),
                    'market_weight': Decimal('0.30'),
                    'legal_weight': Decimal('0.20'),
                    'cultural_weight': Decimal('0.10'),
                    'operational_weight': Decimal('0.20'),
                }
            },
            {
                'name': 'Agriculture',
                'description': 'Agriculture industry',
                'default_risk_level': 'medium',
                'weights': {
                    'financial_weight': Decimal('0.25'),
                    'market_weight': Decimal('0.20'),
                    'legal_weight': Decimal('0.10'),
                    'cultural_weight': Decimal('0.25'),
                    'operational_weight': Decimal('0.20'),
                }
            },
            {
                'name': 'Service',
                'description': 'Service industry',
                'default_risk_level': 'low',
                'weights': {
                    'financial_weight': Decimal('0.20'),
                    'market_weight': Decimal('0.25'),
                    'legal_weight': Decimal('0.15'),
                    'cultural_weight': Decimal('0.20'),
                    'operational_weight': Decimal('0.20'),
                }
            },
        ]

        for i in industries:
            ind_obj, created = Industry.objects.update_or_create(
                name=i['name'],
                defaults={'description': i['description'], 'default_risk_level': i['default_risk_level']}
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(f"{action} industry: {ind_obj}")

            weights = i['weights']
            w_obj, w_created = IndustryRiskWeight.objects.update_or_create(
                industry=ind_obj,
                defaults={
                    'financial_weight': weights['financial_weight'],
                    'market_weight': weights['market_weight'],
                    'legal_weight': weights['legal_weight'],
                    'cultural_weight': weights['cultural_weight'],
                    'operational_weight': weights['operational_weight'],
                }
            )
            self.stdout.write(f"{('Created' if w_created else 'Updated')} weights for: {ind_obj.name}")

        self.stdout.write(self.style.SUCCESS('Seeding complete'))
