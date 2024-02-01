from django.contrib.auth.hashers import make_password, check_password
# from django.http.response import HttpResponse
# from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import (permissions, status,
                            # viewsets, mixins
                            )
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import (CustomUserSerializer)
from users.models import User
from rest_framework.pagination import PageNumberPagination
# from .permissions import AuthorOnly
# from django.db.models import F, Sum


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
