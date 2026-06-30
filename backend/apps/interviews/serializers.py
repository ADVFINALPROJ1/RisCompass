from rest_framework import serializers
from .models import InterviewSession, InterviewQuestion, InterviewAnswer, AILocalInsight


class InterviewQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewQuestion
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class InterviewAnswerSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.question_text', read_only=True)
    
    class Meta:
        model = InterviewAnswer
        fields = '__all__'
        read_only_fields = ('id', 'created_at')


class InterviewSessionSerializer(serializers.ModelSerializer):
    answers = InterviewAnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = InterviewSession
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class InterviewSessionDetailSerializer(serializers.ModelSerializer):
    answers = InterviewAnswerSerializer(many=True, read_only=True)
    ai_insight = serializers.SerializerMethodField()
    
    class Meta:
        model = InterviewSession
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_ai_insight(self, obj):
        try:
            insight = obj.ai_insight
            return AILocalInsightSerializer(insight).data
        except AILocalInsight.DoesNotExist:
            return None


class AILocalInsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = AILocalInsight
        fields = '__all__'
        read_only_fields = ('id', 'created_at')


class InterviewSessionWithQuestionsSerializer(serializers.ModelSerializer):
    """Serializer for GET /api/interviews/<session_id>/ - returns session and questions"""
    questions = serializers.SerializerMethodField()
    answers = InterviewAnswerSerializer(many=True, read_only=True)
    risk_report_id = serializers.SerializerMethodField()
    
    class Meta:
        model = InterviewSession
        fields = ['id', 'snapshot', 'status', 'trigger_reason', 'started_at', 
                  'completed_at', 'created_at', 'updated_at', 'questions', 'answers', 'risk_report_id']
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_questions(self, obj):
        """Get questions relevant to the snapshot's industry"""
        industry = obj.snapshot.industry
        questions = InterviewQuestion.objects.filter(
            industry__isnull=True
        ) | InterviewQuestion.objects.filter(
            industry=industry
        )
        questions = questions.filter(is_active=True).distinct()
        return InterviewQuestionSerializer(questions, many=True).data
    
    def get_risk_report_id(self, obj):
        """Get the risk report ID if the interview is completed"""
        if obj.status == InterviewSession.STATUS_COMPLETED:
            try:
                from apps.risks.models import RiskReport
                report = RiskReport.objects.filter(snapshot=obj.snapshot).latest('created_at')
                return report.id
            except RiskReport.DoesNotExist:
                return None
        return None


class AnswerCreateSerializer(serializers.Serializer):
    """Serializer for creating/updating answers"""
    question_id = serializers.IntegerField()
    answer_text = serializers.CharField(required=False, allow_blank=True)
    answer_value = serializers.IntegerField(required=False, allow_null=True)


class BulkAnswerSerializer(serializers.Serializer):
    """Serializer for POST /api/interviews/<session_id>/answers/"""
    answers = AnswerCreateSerializer(many=True)


class InterviewCompleteSerializer(serializers.Serializer):
    """Serializer for POST /api/interviews/<session_id>/complete/ response"""
    ai_insight = AILocalInsightSerializer()
    risk_report = serializers.DictField()
