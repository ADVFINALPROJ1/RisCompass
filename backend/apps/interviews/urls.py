from django.urls import path
from .views import get_interview_session, save_answers, complete_interview

urlpatterns = [
    path('<int:session_id>/', get_interview_session, name='interview-session-detail'),
    path('<int:session_id>/answers/', save_answers, name='interview-save-answers'),
    path('<int:session_id>/complete/', complete_interview, name='interview-complete'),
]
