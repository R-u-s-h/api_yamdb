from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, GenreViewSet, ReviewViewSet, TitleViewSet

v1_router = routers.DefaultRouter()
v1_router.register("categories", CategoryViewSet, basename="api-categories")
v1_router.register("genres", GenreViewSet, basename="api-genres")
v1_router.register("titles", TitleViewSet, basename="api-titles")
v1_router.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet,
    basename="api-reviews",
)

urlpatterns = [
    path("v1/", include(v1_router.urls)),
]
