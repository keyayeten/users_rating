from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    CustomUserViewSet,
    PostViewSet
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
]
