from rest_framework import serializers
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password
from account.models import CustomUser, VerificationCode, Subscription


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'phone',
            'first_name', 'last_name', 'password',
            'password2'
        ]

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': "Passwords do not match"})
        try:
            validate_password(data['password'])
        except exceptions.ValidationError as error:
            raise serializers.ValidationError({'password': list(error.messages)})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
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
                raise serializers.ValidationError({"code": "Verification code expired"})
            if verification.code != data['code']:
                raise serializers.ValidationError({"code": "Invalid verification code"})
            data['user'] = user
            return data
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"email": "User with this email does not exist"})
        except VerificationCode.DoesNotExist:
            raise serializers.ValidationError({"code": "Verification code not found"})


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'photo']


class CustomUserSerializer(serializers.ModelSerializer):
    subscriptions = serializers.SerializerMethodField()
    subscriptions_count = serializers.SerializerMethodField()
    subscribers = serializers.SerializerMethodField()
    subscribers_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'first_name', 'last_name', 'middle_name',
            'email', 'phone', 'photo', 'date_of_birth', 'about',
            'is_private', 'is_verified', 'subscriptions',
            'subscribers', 'subscriptions_count', 'subscribers_count'
        ]

    def get_subscriptions(self, obj):
        subscriptions = obj.get_subscriptions()
        return UserShortSerializer(subscriptions, many=True).data

    def get_subscribers(self, obj):
        subscribers = obj.get_subscribers()
        return UserShortSerializer(subscribers, many=True).data

    def get_subscriptions_count(self, obj):
        return obj.get_subscriptions().count()

    def get_subscribers_count(self, obj):
        return obj.get_subscribers().count()