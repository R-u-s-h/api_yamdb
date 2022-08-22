from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Comment, Genre, Review, Title, User

from .permissions import (
    IsAdmin,
    IsModerator,
    IsOwner,
    PermissionPerMethodMixin,
    ReadOnly,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleCreateSerializer,
    TitleSerializer,
    UserEditSerializer,
    UserSerializer,
    UserSignupConfirmSerializer,
    UserSignupSerializer,
)


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class CategoryGenreFilter(filters.FilterSet):
    category = CharFilterInFilter(
        field_name='category__slug',
        lookup_expr='in'
    )
    genre = CharFilterInFilter(field_name='genre__slug', lookup_expr='in')
    year = filters.NumberFilter(field_name='year', lookup_expr='contains')
    name = filters.Filter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'year', 'name']


class CategoryViewSet(PermissionPerMethodMixin, ListCreateDestroyViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "slug"
    permission_classes_per_method = {
        "list": [ReadOnly],
        "create": [IsAdmin],
        "destroy": [IsAdmin],
    }
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    pagination_class = LimitOffsetPagination


class GenreViewSet(PermissionPerMethodMixin, ListCreateDestroyViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    lookup_field = "slug"
    permission_classes_per_method = {
        "list": [ReadOnly],
        "create": [IsAdmin],
        "destroy": [IsAdmin],
    }
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    pagination_class = LimitOffsetPagination


class TitleViewSet(PermissionPerMethodMixin, viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    permission_classes_per_method = {
        "list": [ReadOnly],
        "partial_update": [IsAdmin],
        "create": [IsAdmin],
        "destroy": [IsAdmin],
    }
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CategoryGenreFilter
    filterset_fields = ("name", "year", "category__slug", "genre__slug")
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "list":
            return TitleSerializer
        return TitleCreateSerializer


class ReviewViewSet(PermissionPerMethodMixin, viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes_per_method = {
        "create": [IsAuthenticated],
        "list": [ReadOnly],
        "retrieve": [ReadOnly],
        "partial_update": [IsOwner | IsModerator | IsAdmin],
        "destroy": [IsOwner | IsModerator | IsAdmin],
    }

    def get_queryset(self, *args, **kwargs):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)

        # Validate that user can post a single review only
        if Review.objects.filter(
            title=title, author=self.request.user
        ).exists():
            raise serializers.ValidationError(
                "Пользователь может оставить только один отзыв "
                "на произведение"
            )

        serializer.save(title=title, author=self.request.user)


class CommentViewSet(PermissionPerMethodMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes_per_method = {
        "create": [IsAuthenticated],
        "list": [ReadOnly],
        "retrieve": [ReadOnly],
        "partial_update": [IsOwner | IsModerator | IsAdmin],
        "destroy": [IsOwner | IsModerator | IsAdmin],
    }

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
    permission_classes = [IsAdmin | IsAdminUser]
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
