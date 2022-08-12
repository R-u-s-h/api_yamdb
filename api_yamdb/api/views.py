from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
)
from rest_framework import viewsets
from reviews.models import Category, Genre, Title


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
