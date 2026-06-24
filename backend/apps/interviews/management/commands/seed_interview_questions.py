from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Seed interview questions for different industries'

    def handle(self, *args, **options):
        from apps.interviews.models import InterviewQuestion
        from apps.industries.models import Industry

        # Get industries
        retail = Industry.objects.get(name='Retail')
        tech = Industry.objects.get(name='Tech')
        agriculture = Industry.objects.get(name='Agriculture')
        service = Industry.objects.get(name='Service')

        # Retail questions (5 questions)
        retail_questions = [
            {
                'question_text': 'What is your primary source of inventory funding?',
                'question_type': InterviewQuestion.QUESTION_TYPE_TEXT,
                'risk_category': InterviewQuestion.RISK_CATEGORY_FINANCIAL,
            },
            {
                'question_text': 'How do you handle supply chain disruptions?',
                'question_type': InterviewQuestion.QUESTION_TYPE_MULTIPLE_CHOICE,
                'risk_category': InterviewQuestion.RISK_CATEGORY_OPERATIONAL,
            },
            {
                'question_text': 'On a scale of 1-10, how stable is your local customer base?',
                'question_type': InterviewQuestion.QUESTION_TYPE_SCALE,
                'risk_category': InterviewQuestion.RISK_CATEGORY_MARKET,
            },
            {
                'question_text': 'Do you have all necessary business licenses and permits?',
                'question_type': InterviewQuestion.QUESTION_TYPE_YES_NO,
                'risk_category': InterviewQuestion.RISK_CATEGORY_LEGAL,
            },
            {
                'question_text': 'How do you adapt to local cultural preferences in your product offerings?',
                'question_type': InterviewQuestion.QUESTION_TYPE_TEXT,
                'risk_category': InterviewQuestion.RISK_CATEGORY_CULTURAL,
            },
        ]

        # Tech questions (5 questions)
        tech_questions = [
            {
                'question_text': 'What is your current monthly burn rate?',
                'question_type': InterviewQuestion.QUESTION_TYPE_TEXT,
                'risk_category': InterviewQuestion.RISK_CATEGORY_FINANCIAL,
            },
            {
                'question_text': 'How do you protect your intellectual property?',
                'question_type': InterviewQuestion.QUESTION_TYPE_MULTIPLE_CHOICE,
                'risk_category': InterviewQuestion.RISK_CATEGORY_LEGAL,
            },
            {
                'question_text': 'On a scale of 1-10, how competitive is your target market?',
                'question_type': InterviewQuestion.QUESTION_TYPE_SCALE,
                'risk_category': InterviewQuestion.RISK_CATEGORY_MARKET,
            },
            {
                'question_text': 'Do you have a disaster recovery plan for your systems?',
                'question_type': InterviewQuestion.QUESTION_TYPE_YES_NO,
                'risk_category': InterviewQuestion.RISK_CATEGORY_OPERATIONAL,
            },
            {
                'question_text': 'How do you ensure your product fits local cultural norms?',
                'question_type': InterviewQuestion.QUESTION_TYPE_TEXT,
                'risk_category': InterviewQuestion.RISK_CATEGORY_CULTURAL,
            },
        ]

        # Agriculture questions (5 questions)
        agriculture_questions = [
            {
                'question_text': 'What is your primary source of financing for equipment and seeds?',
                'question_type': InterviewQuestion.QUESTION_TYPE_TEXT,
                'risk_category': InterviewQuestion.RISK_CATEGORY_FINANCIAL,
            },
            {
                'question_text': 'How do you manage weather-related risks?',
                'question_type': InterviewQuestion.QUESTION_TYPE_MULTIPLE_CHOICE,
                'risk_category': InterviewQuestion.RISK_CATEGORY_OPERATIONAL,
            },
            {
                'question_text': 'On a scale of 1-10, how volatile are your crop prices?',
                'question_type': InterviewQuestion.QUESTION_TYPE_SCALE,
                'risk_category': InterviewQuestion.RISK_CATEGORY_MARKET,
            },
            {
                'question_text': 'Do you have clear land ownership documentation?',
                'question_type': InterviewQuestion.QUESTION_TYPE_YES_NO,
                'risk_category': InterviewQuestion.RISK_CATEGORY_LEGAL,
            },
            {
                'question_text': 'How do traditional farming practices influence your operations?',
                'question_type': InterviewQuestion.QUESTION_TYPE_TEXT,
                'risk_category': InterviewQuestion.RISK_CATEGORY_CULTURAL,
            },
        ]

        # Service questions (4 questions)
        service_questions = [
            {
                'question_text': 'What is your average client payment cycle?',
                'question_type': InterviewQuestion.QUESTION_TYPE_TEXT,
                'risk_category': InterviewQuestion.RISK_CATEGORY_FINANCIAL,
            },
            {
                'question_text': 'How do you ensure service quality consistency?',
                'question_type': InterviewQuestion.QUESTION_TYPE_MULTIPLE_CHOICE,
                'risk_category': InterviewQuestion.RISK_CATEGORY_OPERATIONAL,
            },
            {
                'question_text': 'On a scale of 1-10, how dependent are you on a few key clients?',
                'question_type': InterviewQuestion.QUESTION_TYPE_SCALE,
                'risk_category': InterviewQuestion.RISK_CATEGORY_MARKET,
            },
            {
                'question_text': 'Do you have proper service contracts with your clients?',
                'question_type': InterviewQuestion.QUESTION_TYPE_YES_NO,
                'risk_category': InterviewQuestion.RISK_CATEGORY_LEGAL,
            },
        ]

        # Seed questions for each industry
        industry_data = [
            (retail, retail_questions, 'Retail'),
            (tech, tech_questions, 'Tech'),
            (agriculture, agriculture_questions, 'Agriculture'),
            (service, service_questions, 'Service'),
        ]

        total_created = 0
        for industry, questions, industry_name in industry_data:
            for q_data in questions:
                question, created = InterviewQuestion.objects.get_or_create(
                    industry=industry,
                    question_text=q_data['question_text'],
                    defaults={
                        'question_type': q_data['question_type'],
                        'risk_category': q_data['risk_category'],
                    }
                )
                if created:
                    total_created += 1
                    self.stdout.write(f"Created question for {industry_name}: {question.question_text[:50]}...")
                else:
                    self.stdout.write(f"Question already exists for {industry_name}: {question.question_text[:50]}...")

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {total_created} interview questions'))
