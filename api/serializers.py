import re
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers, status
# from rest_framework.validators import (UniqueTogetherValidator,
#                                        ValidationError)
from users.models import User
# from django.core.exceptions import PermissionDenied


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name',
                  'last_name', 'password']

    @staticmethod
    def invalid_character(value):
        match = re.search(r'[^a-zA-Z0-9.@+\-_]', value)
        if match:
            return match.group()
        return None

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError("Имя 'me' недопустимо",
                                              code=status.HTTP_400_BAD_REQUEST)
        if not re.match(r'^[\w.@+-]+$', value):
            raise serializers.ValidationError(
                (f"Имя пользователя не соответствует требуемому формату. "
                 f"Содержится лишний символ {self.invalid_character(value)}"),
                code='invalid_username')
        return value


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name'
        ]
