from rest_framework import serializers

from account.models import CustomUser


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['username', 'photo']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['username', 'first_name', 'last_name',
                  'email', 'photo', 'middle_name', 'date_of_birth',
                  'about']