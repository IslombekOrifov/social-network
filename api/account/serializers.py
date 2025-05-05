from rest_framework import serializers
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password
from account.models import CustomUser, VerificationCode


class UserCeateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'phone',
            'first_name', 'last_name', 'password',
            'password2'
        ]
    
    def validate_password(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': "Password not similar"})
        try:
            validate_password(data['password'])
        except exceptions.ValidationError as error:
            raise serializers.ValidationError({'password': list(error.messages)})
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objecs.create_user(**validated_data)
        VerificationCode.create_verification_code(user)
        return user


class VerifyUserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = CustomUser.objects.get(email=data['email'])
            verification = VerificationCode.objects.get(user=user)
            if not verification.is_valid():
                raise serializers.ValidationError("verification code expired")
            if verification.code != data['code']:
                raise serializers.ValidationError('Wrong verification code')
        except (CustomUser.DoesNotExist, VerificationCode.DoesNotExist):
            raise serializers.ValidationError('Wrong email or verification code')


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['username', 'photo']


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'username', 'first_name', 'last_name',
            'email', 'phone', 'photo', 'middle_name', 
            'date_of_birth', 'about'
        ]