from django_filters import rest_framework as filters

from reviews.models import Title


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class CategoryGenreFilter(filters.FilterSet):
    category = CharFilterInFilter(
        field_name="category__slug", lookup_expr="in"
    )
    genre = CharFilterInFilter(field_name="genre__slug", lookup_expr="in")
    year = filters.NumberFilter(field_name="year", lookup_expr="contains")
    name = filters.Filter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Title
        fields = ("category", "genre", "year", "name",)
