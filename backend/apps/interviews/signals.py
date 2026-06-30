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
    Automatically create an interview session for every business snapshot created.
    This allows users to optionally complete interviews for any snapshot to enhance risk assessment.
    """
    if created:
        should_trigger, reason = should_trigger_interview(instance)
        trigger_reason = reason if should_trigger else 'Optional interview for enhanced risk assessment'
        InterviewSession.objects.create(
            snapshot=instance,
            trigger_reason=trigger_reason
        )
