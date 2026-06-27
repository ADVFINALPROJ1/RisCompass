from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import InterviewSession, InterviewQuestion, InterviewAnswer, AILocalInsight
from .serializers import (
    InterviewSessionWithQuestionsSerializer,
    BulkAnswerSerializer,
    InterviewAnswerSerializer,
    AILocalInsightSerializer
)
from .services.gemini_service import GeminiService
from apps.snapshots.models import BusinessSnapshot
from apps.risks.models import RiskReport, RiskFactor
from apps.risks.serializers import RiskReportSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_interview_session(request, session_id):
    """
    Get interview session and questions.
    
    GET /api/interviews/<session_id>/
    """
    try:
        session = InterviewSession.objects.get(id=session_id)
    except InterviewSession.DoesNotExist:
        return Response(
            {'detail': 'Interview session not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check if user owns the snapshot linked to this session
    if session.snapshot.user != request.user:
        return Response(
            {'detail': 'You do not have permission to access this interview session.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = InterviewSessionWithQuestionsSerializer(session)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_answers(request, session_id):
    """
    Save answers for an interview session.
    
    POST /api/interviews/<session_id>/answers/
    Body: {
        "answers": [
            {"question_id": 1, "answer_text": "...", "answer_value": 5},
            ...
        ]
    }
    """
    try:
        session = InterviewSession.objects.get(id=session_id)
    except InterviewSession.DoesNotExist:
        return Response(
            {'detail': 'Interview session not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check if user owns the snapshot linked to this session
    if session.snapshot.user != request.user:
        return Response(
            {'detail': 'You do not have permission to modify this interview session.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Validate request data
    serializer = BulkAnswerSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'detail': 'Invalid request data.', 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Save or update answers
    answers_data = serializer.validated_data['answers']
    created_answers = []
    
    for answer_data in answers_data:
        question_id = answer_data['question_id']
        
        # Validate question exists
        try:
            question = InterviewQuestion.objects.get(id=question_id)
        except InterviewQuestion.DoesNotExist:
            return Response(
                {'detail': f'Question with id {question_id} not found.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create or update answer
        answer, created = InterviewAnswer.objects.update_or_create(
            session=session,
            question=question,
            defaults={
                'answer_text': answer_data.get('answer_text', ''),
                'answer_value': answer_data.get('answer_value')
            }
        )
        created_answers.append(answer)
    
    # Update session status if not already in progress
    if session.status == InterviewSession.STATUS_NOT_STARTED:
        session.status = InterviewSession.STATUS_IN_PROGRESS
        session.started_at = None  # Will be set when first answer is saved
        if not session.started_at:
            from django.utils import timezone
            session.started_at = timezone.now()
        session.save()
    
    # Return updated answers
    response_serializer = InterviewAnswerSerializer(created_answers, many=True)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_interview(request, session_id):
    """
    Complete interview session:
    1. Call Gemini service to generate AI insights
    2. Save AILocalInsight
    3. Generate final RiskReport using AI signals
    4. Return final report
    
    POST /api/interviews/<session_id>/complete/
    """
    try:
        session = InterviewSession.objects.get(id=session_id)
    except InterviewSession.DoesNotExist:
        return Response(
            {'detail': 'Interview session not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check if user owns the snapshot linked to this session
    if session.snapshot.user != request.user:
        return Response(
            {'detail': 'You do not have permission to complete this interview session.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Check if session is already completed
    if session.status == InterviewSession.STATUS_COMPLETED:
        return Response(
            {'detail': 'Interview session is already completed.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get snapshot data
    snapshot = session.snapshot
    
    # Get questions and answers
    answers = session.answers.all()
    if not answers.exists():
        return Response(
            {'detail': 'No answers found for this session. Please provide answers before completing.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Prepare data for Gemini service
    snapshot_data = {
        'company_name': snapshot.title,
        'industry': snapshot.industry.name if snapshot.industry else 'N/A',
        'region': snapshot.region.region_name if snapshot.region else 'N/A',
        'description': snapshot.description
    }
    
    questions_data = []
    for answer in answers:
        questions_data.append({
            'id': answer.question.id,
            'question_text': answer.question.question_text,
            'risk_category': answer.question.risk_category
        })
    
    answers_data = []
    for answer in answers:
        answers_data.append({
            'question_id': answer.question.id,
            'answer_text': answer.answer_text,
            'answer_value': answer.answer_value
        })
    
    # Call Gemini service
    try:
        gemini_service = GeminiService()
        insights = gemini_service.generate_insights(
            snapshot=snapshot_data,
            questions=questions_data,
            answers=answers_data
        )
    except Exception as e:
        return Response(
            {'detail': f'Failed to generate AI insights: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Save AILocalInsight
    ai_insight, created = AILocalInsight.objects.update_or_create(
        session=session,
        defaults={
            'summary': insights.get('summary', ''),
            'financial_risk_signal': str(insights.get('financial_risk_signal', 50)),
            'market_risk_signal': str(insights.get('market_risk_signal', 50)),
            'legal_risk_signal': str(insights.get('legal_risk_signal', 50)),
            'cultural_risk_signal': str(insights.get('cultural_risk_signal', 50)),
            'operational_risk_signal': str(insights.get('operational_risk_signal', 50)),
            'recommended_warnings': insights.get('recommended_warnings', []),
            'model_name': 'gemini-2.0-flash-exp'
        }
    )
    
    # Generate final RiskReport using AI signals
    # Convert string signals back to integers for calculation
    financial_risk = int(insights.get('financial_risk_signal', 50))
    market_risk = int(insights.get('market_risk_signal', 50))
    legal_risk = int(insights.get('legal_risk_signal', 50))
    cultural_risk = int(insights.get('cultural_risk_signal', 50))
    operational_risk = int(insights.get('operational_risk_signal', 50))
    
    # Calculate overall risk score
    overall_risk_score = (
        financial_risk + market_risk + legal_risk + 
        cultural_risk + operational_risk
    ) // 5
    
    # Calculate confidence score based on number of answers
    total_questions = InterviewQuestion.objects.filter(is_active=True).count()
    confidence_score = min(100, (len(answers) * 100) // max(1, total_questions))
    
    # Determine confidence label
    if confidence_score >= 80:
        confidence_label = 'High'
    elif confidence_score >= 50:
        confidence_label = 'Medium'
    else:
        confidence_label = 'Low'
    
    # Generate summary and recommendation
    summary = insights.get('summary', '')
    recommendation = _generate_recommendation_from_warnings(
        insights.get('recommended_warnings', [])
    )
    
    # Create RiskReport
    try:
        risk_report = RiskReport.objects.create(
            snapshot=snapshot,
            overall_risk_score=overall_risk_score,
            confidence_score=confidence_score,
            confidence_label=confidence_label,
            financial_risk=financial_risk,
            market_risk=market_risk,
            legal_risk=legal_risk,
            cultural_risk=cultural_risk,
            operational_risk=operational_risk,
            summary=summary,
            recommendation=recommendation,
            data_sources_used=['ai_interview']
        )
    except Exception as e:
        return Response(
            {'detail': f'Failed to create risk report: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Create RiskFactors from AI insights
    try:
        _create_ai_risk_factors(risk_report, insights)
    except Exception as e:
        return Response(
            {'detail': f'Failed to create risk factors: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Update session status
    try:
        session.status = InterviewSession.STATUS_COMPLETED
        from django.utils import timezone
        session.completed_at = timezone.now()
        session.save()
    except Exception as e:
        return Response(
            {'detail': f'Failed to update session status: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Return response
    try:
        ai_insight_serializer = AILocalInsightSerializer(ai_insight)
        risk_report_serializer = RiskReportSerializer(risk_report)
    except Exception as e:
        return Response(
            {'detail': f'Failed to serialize response: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response({
        'ai_insight': ai_insight_serializer.data,
        'risk_report': risk_report_serializer.data
    }, status=status.HTTP_201_CREATED)


def _generate_recommendation_from_warnings(warnings):
    """Generate recommendation from AI warnings"""
    if not warnings:
        return "No specific warnings. Business appears to be in good standing based on interview responses."
    
    if len(warnings) == 1:
        return f"Warning: {warnings[0]}. Please review this area carefully."
    
    recommendation = "Several areas require attention:\n"
    for i, warning in enumerate(warnings, 1):
        recommendation += f"{i}. {warning}\n"
    
    recommendation += "Consider addressing these areas before proceeding with business operations."
    return recommendation


def _create_ai_risk_factors(risk_report, insights):
    """Create RiskFactor instances from AI insights"""
    risk_categories = [
        ('financial', insights.get('financial_risk_signal', 50)),
        ('market', insights.get('market_risk_signal', 50)),
        ('legal', insights.get('legal_risk_signal', 50)),
        ('cultural', insights.get('cultural_risk_signal', 50)),
        ('operational', insights.get('operational_risk_signal', 50))
    ]
    
    category_map = {
        'financial': RiskFactor.CATEGORY_FINANCIAL,
        'market': RiskFactor.CATEGORY_MARKET,
        'legal': RiskFactor.CATEGORY_LEGAL,
        'cultural': RiskFactor.CATEGORY_CULTURAL,
        'operational': RiskFactor.CATEGORY_OPERATIONAL
    }
    
    for category_name, score in risk_categories:
        RiskFactor.objects.create(
            report=risk_report,
            category=category_map[category_name],
            name=f'{category_name.capitalize()} Risk (AI Interview)',
            score=int(score),
            explanation=f'Risk score derived from AI interview analysis',
            source_type=RiskFactor.SOURCE_TYPE_AI_INTERVIEW
        )
