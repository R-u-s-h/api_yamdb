<<<<<<< Updated upstream
=======
from rest_framework import viewsets, filters

>>>>>>> Stashed changes
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
)
from rest_framework import filters, viewsets
from reviews.models import Category, Genre, Title


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug',)


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
