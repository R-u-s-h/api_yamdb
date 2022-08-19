from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
    signup,
    signup_confirm,
)

v1_router = routers.DefaultRouter()
v1_router.register("categories", CategoryViewSet, basename="api-categories")
v1_router.register("genres", GenreViewSet, basename="api-genres")
v1_router.register("titles", TitleViewSet, basename="api-titles")
v1_router.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet,
    basename="api-reviews",
)
v1_router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="api-comments",
)
v1_router.register("users", UserViewSet, basename="api-users")

auth_urls = [
    url("token/", signup_confirm),
    url("signup/", signup),
]

urlpatterns = [
    path("v1/auth/", include(auth_urls)),
    path("v1/", include(v1_router.urls)),
]
