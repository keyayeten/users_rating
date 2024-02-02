from django.contrib.auth.hashers import make_password, check_password
from djoser.views import UserViewSet
from .permissions import IsAuthorOrReadOnly
from rest_framework import (permissions, status,
                            viewsets)
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import (
    CustomUserSerializer,
    PostSerializer,
    PostRatingSerializer
    )
from users.models import User
from posts.models import Post, PostRating
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = 100


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    def retrieve(self, request, *args, **kwargs):
        if request.user.is_anonymous and request.path.endswith('/me/'):
            return Response({'Ошибка': 'Неавторизован'},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().retrieve(request, *args, **kwargs)

    @action(methods=['POST'],
            detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def set_password(self, request):
        user = self.request.user
        if user.is_authenticated:
            new_password = request.data.get('new_password')
            current_password = request.data.get('current_password')
            if not current_password:
                return Response(
                    {'Ошибка': 'Поле "текущий пароль" обязательно'},
                    status=status.HTTP_400_BAD_REQUEST)
            if not new_password:
                return Response(
                    {'Ошибка': 'Поле "новый пароль" обязательно'},
                    status=status.HTTP_400_BAD_REQUEST)
            if not check_password(current_password, user.password):
                return Response(
                    {'Ошибка': 'Текущий пароль некорректен'},
                    status=status.HTTP_400_BAD_REQUEST)
            user.password = make_password(new_password)
            user.save()
            return Response({'Статус': 'пароль установлен'},
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'Ошибка': 'Неавторизован'},
                            status=status.HTTP_401_UNAUTHORIZED)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorOrReadOnly]
        return super().get_permissions()

    @action(detail=True, methods=['post', 'patch', 'delete'])
    def rating(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            serializer = PostRatingSerializer(
                data=request.data,
                partial=False,
                context={'request': request})
        elif request.method == "PATCH":
            rating = get_object_or_404(
                PostRating,
                post=post,
                user=request.user)
            serializer = PostRatingSerializer(
                instance=rating,
                data=request.data,
                partial=False,
                context={'request': request})
        elif request.method == "DELETE":
            rating = get_object_or_404(
                PostRating,
                post=post,
                user=request.user)
            rating.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
