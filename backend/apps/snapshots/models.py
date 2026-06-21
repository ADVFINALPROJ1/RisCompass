from django.conf import settings
from django.db import models


class BusinessSnapshot(models.Model):
    BUSINESS_STAGE_IDEA = 'idea'
    BUSINESS_STAGE_STARTUP = 'startup'
    BUSINESS_STAGE_EXISTING = 'existing_business'
    BUSINESS_STAGE_PIVOT = 'pivot'
    BUSINESS_STAGE_EXPANSION = 'expansion'

    BUSINESS_STAGE_CHOICES = [
        (BUSINESS_STAGE_IDEA, 'Idea'),
        (BUSINESS_STAGE_STARTUP, 'Startup'),
        (BUSINESS_STAGE_EXISTING, 'Existing Business'),
        (BUSINESS_STAGE_PIVOT, 'Pivot'),
        (BUSINESS_STAGE_EXPANSION, 'Expansion'),
    ]

    BUSINESS_SIZE_MICRO = 'micro'
    BUSINESS_SIZE_SMALL = 'small'
    BUSINESS_SIZE_MEDIUM = 'medium'

    BUSINESS_SIZE_CHOICES = [
        (BUSINESS_SIZE_MICRO, 'Micro'),
        (BUSINESS_SIZE_SMALL, 'Small'),
        (BUSINESS_SIZE_MEDIUM, 'Medium'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='business_snapshots'
    )
    industry = models.ForeignKey(
        'industries.Industry',
        on_delete=models.CASCADE,
        related_name='business_snapshots'
    )
    region = models.ForeignKey(
        'regions.Region',
        on_delete=models.CASCADE,
        related_name='business_snapshots'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    business_stage = models.CharField(
        max_length=32,
        choices=BUSINESS_STAGE_CHOICES,
        default=BUSINESS_STAGE_IDEA,
    )
    startup_budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    currency = models.CharField(max_length=16, blank=True)
    target_customer = models.TextField(blank=True)
    business_size = models.CharField(
        max_length=16,
        choices=BUSINESS_SIZE_CHOICES,
        default=BUSINESS_SIZE_MICRO,
    )
    has_physical_location = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.user})"
