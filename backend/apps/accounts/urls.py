from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView,
    CustomTokenObtainPairView,
    current_user,
)

urlpatterns = [
    # Registration
    path('register/', RegisterView.as_view(), name='register'),
    
    # Login (obtain JWT tokens)
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Refresh token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Current user
    path('me/', current_user, name='current_user'),
]
