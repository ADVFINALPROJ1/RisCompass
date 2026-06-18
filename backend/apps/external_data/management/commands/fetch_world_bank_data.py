from django.core.management.base import BaseCommand
from django.db import transaction
from apps.regions.models import Region
from apps.external_data.models import EconomicIndicator, RegionEconomicData
from apps.external_data.services.world_bank import fetch_world_bank_indicator
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Fetch economic data from World Bank API for all regions and indicators'

    def add_arguments(self, parser):
        parser.add_argument(
            '--country-code',
            type=str,
            help='Specific country code to fetch data for (e.g., US, GB, FR)'
        )
        parser.add_argument(
            '--indicator-code',
            type=str,
            help='Specific indicator code to fetch data for (e.g., FP.CPI.TOTL.ZG)'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=0,
            help='Limit number of regions to process (0 = all)'
        )

    def handle(self, *args, **options):
        country_code = options.get('country_code')
        indicator_code = options.get('indicator_code')
        limit = options.get('limit', 0)

        # Get regions to process
        if country_code:
            regions = Region.objects.filter(country_code=country_code)
            self.stdout.write(
                self.style.WARNING(f"Fetching data for country: {country_code}")
            )
        else:
            regions = Region.objects.filter(is_supported=True)
            self.stdout.write(
                self.style.WARNING(f"Fetching data for all supported regions")
            )

        if limit > 0:
            regions = regions[:limit]
            self.stdout.write(
                self.style.WARNING(f"Limiting to {limit} regions")
            )

        # Get indicators to process
        if indicator_code:
            indicators = EconomicIndicator.objects.filter(code=indicator_code)
            self.stdout.write(
                self.style.WARNING(f"Fetching indicator: {indicator_code}")
            )
        else:
            indicators = EconomicIndicator.objects.all()
            self.stdout.write(
                self.style.WARNING(f"Fetching all indicators")
            )

        total_regions = regions.count()
        total_indicators = indicators.count()
        total_combinations = total_regions * total_indicators

        self.stdout.write(
            self.style.SUCCESS(
                f"Processing {total_regions} regions x {total_indicators} indicators = {total_combinations} combinations"
            )
        )

        success_count = 0
        error_count = 0
        skip_count = 0

        for region in regions:
            for indicator in indicators:
                self.stdout.write(
                    f"Fetching {region.country_code} - {indicator.code}...",
                    ending='\r'
                )

                try:
                    # Fetch data from World Bank API
                    data = fetch_world_bank_indicator(region.country_code, indicator.code)

                    if not data:
                        self.stdout.write(
                            self.style.WARNING(
                                f"  No data returned for {region.country_code} - {indicator.code}"
                            )
                        )
                        skip_count += 1
                        continue

                    # Create or update RegionEconomicData
                    with transaction.atomic():
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

                        if created:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"  Created: {region.country_code} - {indicator.code} ({data['year']}): {data['value']}"
                                )
                            )
                        else:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"  Updated: {region.country_code} - {indicator.code} ({data['year']}): {data['value']}"
                                )
                            )
                        success_count += 1

                except Exception as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(
                            f"  Error fetching {region.country_code} - {indicator.code}: {str(e)}"
                        )
                    )
                    logger.error(
                        f"Error fetching data for {region.country_code} - {indicator.code}: {e}",
                        exc_info=True
                    )

        self.stdout.write('\n')
        self.stdout.write(
            self.style.SUCCESS(
                f"\nSummary: {success_count} successful, {error_count} errors, {skip_count} skipped"
            )
        )
