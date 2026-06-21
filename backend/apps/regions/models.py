from django.db import models


class Region(models.Model):
    REGION_TYPE_URBAN = 'urban'
    REGION_TYPE_SUBURBAN = 'suburban'
    REGION_TYPE_RURAL = 'rural'
    REGION_TYPE_REMOTE = 'remote'

    REGION_TYPE_CHOICES = [
        (REGION_TYPE_URBAN, 'Urban'),
        (REGION_TYPE_SUBURBAN, 'Suburban'),
        (REGION_TYPE_RURAL, 'Rural'),
        (REGION_TYPE_REMOTE, 'Remote'),
    ]

    DATA_HIGH = 'high'
    DATA_MEDIUM = 'medium'
    DATA_LOW = 'low'
    DATA_VERY_LOW = 'very_low'

    DATA_AVAILABILITY_CHOICES = [
        (DATA_HIGH, 'High'),
        (DATA_MEDIUM, 'Medium'),
        (DATA_LOW, 'Low'),
        (DATA_VERY_LOW, 'Very Low'),
    ]

    country_name = models.CharField(max_length=128)
    country_code = models.CharField(max_length=8)
    region_name = models.CharField(max_length=128)
    city_name = models.CharField(max_length=128, blank=True)
    region_type = models.CharField(max_length=20, choices=REGION_TYPE_CHOICES)
    data_availability_level = models.CharField(max_length=20, choices=DATA_AVAILABILITY_CHOICES)
    is_supported = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['country_name', 'region_name']
        constraints = [
            models.UniqueConstraint(fields=['country_code', 'region_name'], name='unique_region_by_country')
        ]

    def __str__(self):
        return f"{self.region_name} ({self.country_code})"
