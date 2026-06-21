from django.core.management.base import BaseCommand
from apps.external_data.models import EconomicIndicator


class Command(BaseCommand):
    help = 'Seed the database with common World Bank economic indicators'

    def handle(self, *args, **options):
        indicators = [
            {
                'code': 'FP.CPI.TOTL.ZG',
                'name': 'Inflation, consumer prices (annual %)',
                'description': 'Annual percentage change in the cost of goods and services',
                'source': 'World Bank',
                'higher_is_riskier': True
            },
            {
                'code': 'SL.UEM.TOTL.ZS',
                'name': 'Unemployment, total (% of total labor force)',
                'description': 'Percentage of total labor force that is unemployed',
                'source': 'World Bank',
                'higher_is_riskier': True
            },
            {
                'code': 'IT.NET.USER.ZS',
                'name': 'Internet users (per 100 people)',
                'description': 'Percentage of individuals using the Internet',
                'source': 'World Bank',
                'higher_is_riskier': False
            },
            {
                'code': 'NY.GDP.MKTP.KD.ZG',
                'name': 'GDP growth (annual %)',
                'description': 'Annual percentage growth rate of GDP at constant market prices',
                'source': 'World Bank',
                'higher_is_riskier': False
            },
            {
                'code': 'FP.WPI.TOTL',
                'name': 'Wholesale price index (2010 = 100)',
                'description': 'Wholesale price index measures changes in prices of goods at wholesale level',
                'source': 'World Bank',
                'higher_is_riskier': True
            },
            {
                'code': 'GC.XPN.TOTL.GD.ZS',
                'name': 'General government final consumption expenditure (% of GDP)',
                'description': 'General government final consumption expenditure as percentage of GDP',
                'source': 'World Bank',
                'higher_is_riskier': False
            },
            {
                'code': 'DT.DOD.DECT.GN.ZS',
                'name': 'External debt stocks (% of GNI)',
                'description': 'Total external debt stocks as percentage of Gross National Income',
                'source': 'World Bank',
                'higher_is_riskier': True
            },
            {
                'code': 'BX.GSR.GNFS.CD',
                'name': 'Exports of goods and services (current US$)',
                'description': 'Total exports of goods and services in current US dollars',
                'source': 'World Bank',
                'higher_is_riskier': False
            },
            {
                'code': 'BM.GSR.GNFS.CD',
                'name': 'Imports of goods and services (current US$)',
                'description': 'Total imports of goods and services in current US dollars',
                'source': 'World Bank',
                'higher_is_riskier': False
            },
            {
                'code': 'SP.POP.TOTL',
                'name': 'Population, total',
                'description': 'Total population of the country',
                'source': 'World Bank',
                'higher_is_riskier': False
            },
        ]

        created_count = 0
        updated_count = 0

        for indicator_data in indicators:
            indicator, created = EconomicIndicator.objects.update_or_create(
                code=indicator_data['code'],
                defaults=indicator_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created indicator: {indicator.name} ({indicator.code})")
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f"Updated indicator: {indicator.name} ({indicator.code})")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully seeded indicators: {created_count} created, {updated_count} updated"
            )
        )
