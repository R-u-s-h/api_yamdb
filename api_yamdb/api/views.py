from rest_framework import filters, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Category, Genre, Review, Title
from django_filters.rest_framework import DjangoFilterBackend

from .permissions import IsAdmin, IsModerator, IsOwnerOrReadOnly
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug',)
    pagination_class = LimitOffsetPagination


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug',)
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'category__slug', 'genre__slug',)
    pagination_class = LimitOffsetPagination


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly | IsAdmin | IsModerator]
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
    ...
