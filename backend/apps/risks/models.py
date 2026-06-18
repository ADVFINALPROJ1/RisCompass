from django.db import models
from apps.snapshots.models import BusinessSnapshot


class RiskReport(models.Model):
    snapshot = models.ForeignKey(
        BusinessSnapshot,
        on_delete=models.CASCADE,
        related_name='risk_reports'
    )
    overall_risk_score = models.IntegerField()
    confidence_score = models.IntegerField()
    confidence_label = models.CharField(max_length=50)
    financial_risk = models.IntegerField()
    market_risk = models.IntegerField()
    legal_risk = models.IntegerField()
    cultural_risk = models.IntegerField()
    operational_risk = models.IntegerField()
    summary = models.TextField(blank=True)
    recommendation = models.TextField(blank=True)
    data_sources_used = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Risk Report'
        verbose_name_plural = 'Risk Reports'

    def __str__(self):
        return f"Risk Report for {self.snapshot.title}"


class RiskFactor(models.Model):
    CATEGORY_FINANCIAL = 'financial'
    CATEGORY_MARKET = 'market'
    CATEGORY_LEGAL = 'legal'
    CATEGORY_CULTURAL = 'cultural'
    CATEGORY_OPERATIONAL = 'operational'

    CATEGORY_CHOICES = [
        (CATEGORY_FINANCIAL, 'Financial'),
        (CATEGORY_MARKET, 'Market'),
        (CATEGORY_LEGAL, 'Legal'),
        (CATEGORY_CULTURAL, 'Cultural'),
        (CATEGORY_OPERATIONAL, 'Operational'),
    ]

    SOURCE_TYPE_EXTERNAL_API = 'external_api'
    SOURCE_TYPE_AI_INTERVIEW = 'ai_interview'
    SOURCE_TYPE_USER_INPUT = 'user_input'
    SOURCE_TYPE_SYSTEM_DEFAULT = 'system_default'

    SOURCE_TYPE_CHOICES = [
        (SOURCE_TYPE_EXTERNAL_API, 'External API'),
        (SOURCE_TYPE_AI_INTERVIEW, 'AI Interview'),
        (SOURCE_TYPE_USER_INPUT, 'User Input'),
        (SOURCE_TYPE_SYSTEM_DEFAULT, 'System Default'),
    ]

    report = models.ForeignKey(
        RiskReport,
        on_delete=models.CASCADE,
        related_name='risk_factors'
    )
    category = models.CharField(
        max_length=32,
        choices=CATEGORY_CHOICES
    )
    name = models.CharField(max_length=255)
    score = models.IntegerField()
    explanation = models.TextField(blank=True)
    source_type = models.CharField(
        max_length=32,
        choices=SOURCE_TYPE_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'name']
        verbose_name = 'Risk Factor'
        verbose_name_plural = 'Risk Factors'

    def __str__(self):
        return f"{self.category}: {self.name} ({self.score})"
