import re
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers, status
# from rest_framework.validators import (UniqueTogetherValidator,
#                                        ValidationError)
from users.models import User
from posts.models import Post, PostRating
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


class PostRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostRating
        fields = ["post", "rating"]

    def create(self, validated_data):
        post_id = validated_data.get('post')
        status = validated_data.get('rating')
        user = self.context['request'].user
        if PostRating.objects.filter(post=post_id, user=user).exists():
            raise serializers.ValidationError("Рейтинг уже поставлен")

        return PostRating.objects.create(
            post=post_id, user=user, rating=status
            )

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()


class PostSerializer(serializers.ModelSerializer):
    votes = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "text",
            "votes",
            "rating"
        ]

    def get_votes(self, obj):
        total_ratings = PostRating.objects.filter(post=obj)
        return total_ratings.count()

    def get_rating(self, obj):
        total_ratings = PostRating.objects.filter(post=obj)
        res = 0
        for rating in total_ratings:
            res += 1 if rating.rating == "+" else -1
        return res
