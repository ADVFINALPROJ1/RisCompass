from django.contrib import admin
from .models import InterviewSession, InterviewQuestion, InterviewAnswer, AILocalInsight


@admin.register(InterviewSession)
class InterviewSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'snapshot', 'status', 'started_at', 'completed_at', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('snapshot__title', 'trigger_reason')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text', 'question_type', 'risk_category', 'industry', 'is_active', 'created_at')
    list_filter = ('question_type', 'risk_category', 'is_active', 'industry')
    search_fields = ('question_text', 'industry__name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(InterviewAnswer)
class InterviewAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'question', 'answer_text', 'answer_value', 'created_at')
    list_filter = ('created_at', 'question__risk_category')
    search_fields = ('session__id', 'question__question_text', 'answer_text')
    readonly_fields = ('created_at',)


@admin.register(AILocalInsight)
class AILocalInsightAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'financial_risk_signal', 'market_risk_signal', 'legal_risk_signal', 'cultural_risk_signal', 'operational_risk_signal', 'model_name', 'created_at')
    list_filter = ('financial_risk_signal', 'market_risk_signal', 'legal_risk_signal', 'cultural_risk_signal', 'operational_risk_signal', 'created_at')
    search_fields = ('session__id', 'model_name', 'summary')
    readonly_fields = ('created_at',)
