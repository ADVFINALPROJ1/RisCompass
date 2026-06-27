"""
Django signals for automatic interview session creation.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver

from .services.trigger import should_trigger_interview
from .models import InterviewSession


@receiver(post_save, sender='snapshots.BusinessSnapshot')
def create_interview_if_triggered(sender, instance, created, **kwargs):
    """
    Automatically create an interview session when a business snapshot is created
    and meets the trigger criteria.
    
    Trigger criteria are defined in should_trigger_interview():
    - Region data availability is low or very_low
    - Region type is rural or remote
    - API data completeness is below 0.60
    - Agriculture industry in remote regions
    """
    if created:
        should_trigger, reason = should_trigger_interview(instance)
        if should_trigger:
            InterviewSession.objects.create(
                snapshot=instance,
                trigger_reason=reason
            )
