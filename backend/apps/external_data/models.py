from django.db import models
from apps.regions.models import Region


class EconomicIndicator(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    source = models.CharField(max_length=255, default='World Bank')
    higher_is_riskier = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Economic Indicator'
        verbose_name_plural = 'Economic Indicators'

    def __str__(self):
        return f"{self.name} ({self.code})"


class RegionEconomicData(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='economic_data')
    indicator = models.ForeignKey(EconomicIndicator, on_delete=models.CASCADE, related_name='region_data')
    year = models.IntegerField()
    value = models.FloatField(null=True, blank=True)
    source = models.CharField(max_length=255, default='World Bank')
    fetched_at = models.DateTimeField(auto_now_add=True)
    is_estimated = models.BooleanField(default=False)

    class Meta:
        ordering = ['-year', 'region', 'indicator']
        verbose_name = 'Region Economic Data'
        verbose_name_plural = 'Region Economic Data'
        constraints = [
            models.UniqueConstraint(
                fields=['region', 'indicator', 'year'],
                name='unique_region_indicator_year'
            )
        ]

    def __str__(self):
        return f"{self.region.country_code} - {self.indicator.code} ({self.year}): {self.value}"
