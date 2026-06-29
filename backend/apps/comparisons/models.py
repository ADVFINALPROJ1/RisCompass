from django.conf import settings
from django.db import models


class Comparison(models.Model):
    FILTER_FOCUS_OVERALL = 'overall'
    FILTER_FOCUS_FINANCIAL = 'financial'
    FILTER_FOCUS_MARKET = 'market'
    FILTER_FOCUS_LEGAL = 'legal'
    FILTER_FOCUS_CULTURAL = 'cultural'
    FILTER_FOCUS_OPERATIONAL = 'operational'

    FILTER_FOCUS_CHOICES = [
        (FILTER_FOCUS_OVERALL, 'Overall'),
        (FILTER_FOCUS_FINANCIAL, 'Financial'),
        (FILTER_FOCUS_MARKET, 'Market'),
        (FILTER_FOCUS_LEGAL, 'Legal'),
        (FILTER_FOCUS_CULTURAL, 'Cultural'),
        (FILTER_FOCUS_OPERATIONAL, 'Operational'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comparisons'
    )
    snapshot_a = models.ForeignKey(
        'snapshots.BusinessSnapshot',
        on_delete=models.CASCADE,
        related_name='comparisons_as_a'
    )
    snapshot_b = models.ForeignKey(
        'snapshots.BusinessSnapshot',
        on_delete=models.CASCADE,
        related_name='comparisons_as_b'
    )
    title = models.CharField(max_length=255)
    filter_focus = models.CharField(
        max_length=32,
        choices=FILTER_FOCUS_CHOICES,
        default=FILTER_FOCUS_OVERALL
    )
    winner_snapshot = models.ForeignKey(
        'snapshots.BusinessSnapshot',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='won_comparisons'
    )
    summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Comparison'
        verbose_name_plural = 'Comparisons'

    def __str__(self):
        return f"{self.title} ({self.user})"
