from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,
    TokenVerifyView
)
from .views import (
    TokenToBlacklistView, RegistrationView,
    VerifyWithEmailView, ResendVerificationCodeView,
    CustomUserProfileAPIView, SubscribeAPIView,
    UnsubscribeAPIView, MySubscriptionsAPIView,
    MySubscribersAPIView
)

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/token/blacklist/', TokenToBlacklistView.as_view(), name='token_verify'),

    path('register/', RegistrationView.as_view(), name='register'),
    path('verify-email/', VerifyWithEmailView.as_view(), name='verify_email'),
    path('resend-verification/', ResendVerificationCodeView.as_view(), name='resend_verification'),

    path('profile/', CustomUserProfileAPIView.as_view(), name='user_profile'),
    path('profile/<int:pk>/', CustomUserProfileAPIView.as_view(), name='user_profile_detail'),
    
    path('subscribe/<int:user_id>/', SubscribeAPIView.as_view(), name='subscribe'),
    path('unsubscribe/<int:user_id>/', UnsubscribeAPIView.as_view(), name='unsubscribe'),
    path('my-subscriptions/', MySubscriptionsAPIView.as_view(), name='my_subscriptions'),
    path('my-subscribers/', MySubscribersAPIView.as_view(), name='my_subscribers'),
]
