from django.urls import path, include
from rest_framework import routers

from api.views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet
)

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
