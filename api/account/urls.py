from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,
    TokenVerifyView
)
from .views import (
    TokenToBlacklistView, RegistrationView,
    VerifyWithEmailView, ResendVerificationCodeView
)

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/token/blacklist/', TokenToBlacklistView.as_view(), name='token_verify'),

    path('register/', RegistrationView.as_view(), name='register'),
    path('verify-email/', VerifyWithEmailView.as_view(), name='verify-email'),
    path('resend-verification/', ResendVerificationCodeView.as_view(), name='resend-verification'),
]
