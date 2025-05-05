from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import CustomUser, VerificationCode
from account.tasks import send_confirm_email
from .serializers import (
    UserCeateSerializer, CustomUserSerializer,
    VerifyUserEmailSerializer
)


class RegistrationView(generics.CreateAPIView):
    serializer_class = UserCeateSerializer
    permission_classes = permissions.AllowAny
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        verification = VerificationCode.objects.get(user=user)
        send_confirm_email(user, verification.code)

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
        user = CustomUser.objects.get(email=serializer.validated_data['email'])
        user.is_verified = True
        user.save()
        VerificationCode.objects.get(user=user).delete()
        return Response(
            {
                'message': 'Email successfully confirmed. You can now log in.'
            },
            status=status.HTTP_200_OK
        )


class ResendVerificationCodeView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get['email']
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
                send_confirm_email(email, verification.code)
                return Response(
                    {
                        'message': "A new verification code has been sent to your email."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except CustomUser.DoesNotExist:
            return Response(
                {
                    'error': 'A user with this email was not found.'
                },
                status=status.HTTP_200_OK
            )


class TokenToBlacklistView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh_token')
        try:
            refresh_token = RefreshToken(refresh_token)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."})
        except Exception as e:
            return Response({"error": str(e)}, status=400)