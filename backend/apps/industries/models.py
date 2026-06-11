from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal


class Industry(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    default_risk_level = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class IndustryRiskWeight(models.Model):
    industry = models.OneToOneField(Industry, on_delete=models.CASCADE, related_name='risk_weight')
    financial_weight = models.DecimalField(max_digits=5, decimal_places=4)
    market_weight = models.DecimalField(max_digits=5, decimal_places=4)
    legal_weight = models.DecimalField(max_digits=5, decimal_places=4)
    cultural_weight = models.DecimalField(max_digits=5, decimal_places=4)
    operational_weight = models.DecimalField(max_digits=5, decimal_places=4)

    def clean(self):
        total = (
            Decimal(self.financial_weight or 0) +
            Decimal(self.market_weight or 0) +
            Decimal(self.legal_weight or 0) +
            Decimal(self.cultural_weight or 0) +
            Decimal(self.operational_weight or 0)
        )
        if total.quantize(Decimal('0.0001')) != Decimal('1.0000'):
            raise ValidationError('Risk weights must sum to 1.00')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Weights for {self.industry.name}"
