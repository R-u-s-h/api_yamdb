from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, status, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import User, Category, Comment, Genre, Review, Title

from .permissions import IsAdmin, IsModerator, IsOwner, ReadOnly
from .serializers import (
    UserSerializer,
    UserEditSerializer,
    UserSignupSerializer,
    UserSignupConfirmSerializer,
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (IsAdmin, ReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("slug",)
    pagination_class = LimitOffsetPagination


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = (IsAdmin, ReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("slug",)
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    permission_classes = (IsAdmin, ReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("name", "year", "category__slug", "genre__slug")
    pagination_class = LimitOffsetPagination


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsOwner | IsModerator | IsAdmin | ReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self, *args, **kwargs):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsOwner | IsModerator | IsAdmin | ReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self, *args, **kwargs):
        title_id = self.kwargs.get("title_id")
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, title_id=title_id, id=review_id)
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, title_id=title_id, id=review_id)
        serializer.save(review=review, author=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = LimitOffsetPagination
    search_fields = ("username",)
    lookup_field = "username"

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        if request.method == "PATCH":
            serializer = UserEditSerializer(request.user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserEditSerializer(request.user)
        return Response(serializer.data)


@api_view(["POST"])
def signup(request):
    """Код подтерждения выводится в консоль."""

    serializer = UserSignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, _ = User.objects.get_or_create(
        defaults={"is_active": False}, **serializer.validated_data
    )
    user.save()
    send_mail(
        "Подтверждение регистрации",
        f"Код подтверждения: {default_token_generator.make_token(user)}",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=True,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def signup_confirm(request):
    try:
        username, confirmation_code = request.data.values()
    except ValueError as err:
        return Response(
            {"Ошибка": f"{err}"}, status=status.HTTP_400_BAD_REQUEST
        )
    user = get_object_or_404(User, username=username)
    serializer = UserSignupConfirmSerializer(user, data=request.data)
    serializer.is_valid(raise_exception=True)
    if not default_token_generator.check_token(user, confirmation_code):
        raise serializers.ValidationError("Неверный confirmation_code")
    user.is_active = True
    user.save()
    token = str(AccessToken.for_user(user))
    return Response(
        {"Ваш токен": token},
        status=status.HTTP_200_OK,
    )
