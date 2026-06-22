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
