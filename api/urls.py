from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import (
    CustomUserViewSet,
    PostViewSet
)

schema_view = get_schema_view(
    openapi.Info(
        title="Users ratings API",
        default_version="v1"
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

app_name = 'api'

router = DefaultRouter()
router.register(r'users',
                CustomUserViewSet,
                basename='users')
router.register(r'posts',
                PostViewSet,
                basename='posts')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    path('swagger/',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),

    path('redoc/',
         schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
