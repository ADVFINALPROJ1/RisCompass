from django.db import models
from django.conf import settings


class InterviewSession(models.Model):
    STATUS_NOT_STARTED = 'not_started'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_NOT_STARTED, 'Not Started'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    snapshot = models.ForeignKey(
        'snapshots.BusinessSnapshot',
        on_delete=models.CASCADE,
        related_name='interview_sessions'
    )
    status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default=STATUS_NOT_STARTED
    )
    trigger_reason = models.TextField(blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Interview Session {self.id} - {self.status}"


class InterviewQuestion(models.Model):
    QUESTION_TYPE_TEXT = 'text'
    QUESTION_TYPE_MULTIPLE_CHOICE = 'multiple_choice'
    QUESTION_TYPE_SCALE = 'scale'
    QUESTION_TYPE_YES_NO = 'yes_no'

    QUESTION_TYPE_CHOICES = [
        (QUESTION_TYPE_TEXT, 'Text'),
        (QUESTION_TYPE_MULTIPLE_CHOICE, 'Multiple Choice'),
        (QUESTION_TYPE_SCALE, 'Scale'),
        (QUESTION_TYPE_YES_NO, 'Yes/No'),
    ]

    RISK_CATEGORY_FINANCIAL = 'financial'
    RISK_CATEGORY_MARKET = 'market'
    RISK_CATEGORY_LEGAL = 'legal'
    RISK_CATEGORY_CULTURAL = 'cultural'
    RISK_CATEGORY_OPERATIONAL = 'operational'

    RISK_CATEGORY_CHOICES = [
        (RISK_CATEGORY_FINANCIAL, 'Financial'),
        (RISK_CATEGORY_MARKET, 'Market'),
        (RISK_CATEGORY_LEGAL, 'Legal'),
        (RISK_CATEGORY_CULTURAL, 'Cultural'),
        (RISK_CATEGORY_OPERATIONAL, 'Operational'),
    ]

    industry = models.ForeignKey(
        'industries.Industry',
        on_delete=models.CASCADE,
        related_name='interview_questions',
        null=True,
        blank=True
    )
    question_text = models.TextField()
    question_type = models.CharField(
        max_length=32,
        choices=QUESTION_TYPE_CHOICES,
        default=QUESTION_TYPE_TEXT
    )
    risk_category = models.CharField(
        max_length=32,
        choices=RISK_CATEGORY_CHOICES
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.question_text[:50]}... ({self.risk_category})"


class InterviewAnswer(models.Model):
    session = models.ForeignKey(
        InterviewSession,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    question = models.ForeignKey(
        InterviewQuestion,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    answer_text = models.TextField(blank=True)
    answer_value = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['question']
        unique_together = ['session', 'question']

    def __str__(self):
        return f"Answer for Question {self.question.id} in Session {self.session.id}"


class AILocalInsight(models.Model):
    session = models.OneToOneField(
        InterviewSession,
        on_delete=models.CASCADE,
        related_name='ai_insight'
    )
    summary = models.TextField(blank=True)
    financial_risk_signal = models.CharField(max_length=32, blank=True)
    market_risk_signal = models.CharField(max_length=32, blank=True)
    legal_risk_signal = models.CharField(max_length=32, blank=True)
    cultural_risk_signal = models.CharField(max_length=32, blank=True)
    operational_risk_signal = models.CharField(max_length=32, blank=True)
    recommended_warnings = models.JSONField(default=dict, blank=True)
    model_name = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"AI Insight for Session {self.session.id}"
