from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import CustomUser, VerificationCode, Subscription
from account.tasks import send_confirm_email
from .serializers import (
    UserShortSerializer, UserCreateSerializer,
    CustomUserSerializer, VerifyUserEmailSerializer
)


class RegistrationView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        verification = VerificationCode.objects.get(user=user)
        send_confirm_email.delay(user.email, verification.code)

        return Response(
            {
                'message': 'Registration successful. Please check your email to confirm your registration.',
                'email': user.email
            },
            status=status.HTTP_201_CREATED
        )


class VerifyWithEmailView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = VerifyUserEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.is_verified = True
        user.save()
        VerificationCode.objects.filter(user=user).delete()
        return Response(
            {
                'message': 'Email successfully confirmed. You can now log in.'
            },
            status=status.HTTP_200_OK
        )


class ResendVerificationCodeView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response(
                {
                    'error': "Email is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = CustomUser.objects.get(email=email)
            if user.is_verified:
                return Response(
                    {
                        'message': "This email already has been verified"
                    },
                    status=status.HTTP_200_OK
                )
            verification = VerificationCode.create_verification_code(user)
            send_confirm_email.delay(user.email, verification.code)
            return Response(
                {
                    'message': "A new verification code has been sent to your email."
                },
                status=status.HTTP_200_OK 
            )
        except CustomUser.DoesNotExist:
            return Response(
                {
                    'error': 'A user with this email was not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )


class TokenToBlacklistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response(
                {"error": "refresh_token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CustomUserProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            user = get_object_or_404(
                CustomUser,
                pk=pk,
                is_active=True,
                is_deleted=False,
                is_verified=True
            )
            if user.is_private and user != request.user:
                return Response(
                    {"detail": "This profile is private."},
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, pk=None):
        user = request.user
        if pk and pk != user.id:
            return Response(
                {"detail": "You can only edit your own profile."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = CustomUserSerializer(
            instance=user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class SubscribeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        target_user = get_object_or_404(
            CustomUser,
            pk=user_id,
            is_active=True,
            is_deleted=False,
            is_verified=True
        )
        if request.user == target_user:
            return Response(
                {'detail': 'You cannot subscribe to yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        subscription, created = Subscription.objects.get_or_create(
            subscriber=request.user,
            target_user=target_user
        )
        
        if not created:
            return Response(
                {'detail': 'You are already subscribed to this user.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        return Response(
            {'detail': 'Successfully subscribed.'},
            status=status.HTTP_201_CREATED
        )


class UnsubscribeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(
            CustomUser,
            pk=user_id,
            is_active=True,
            is_deleted=False
        )
        
        deleted_count, _ = Subscription.objects.filter(
            subscriber=request.user,
            target_user=target_user
        ).delete()
        
        if deleted_count == 0:
            return Response(
                {'detail': 'You are not subscribed to this user.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        return Response(
            {"detail": "Successfully unsubscribed."},
            status=status.HTTP_200_OK
        )


class MySubscriptionsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        subscriptions = request.user.get_subscriptions()
        serializer = UserShortSerializer(subscriptions, many=True)
        return Response(serializer.data)


class MySubscribersAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        subscribers = request.user.get_subscribers()
        serializer = UserShortSerializer(subscribers, many=True)
        return Response(serializer.data)