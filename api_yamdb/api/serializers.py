from rest_framework import relations, serializers, validators
from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    queryset = Category.objects.all()

    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    queryset = Genre.objects.all()

    class Meta:
        model = Genre
        fields = ("name", "slug")


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=False)
    genre = GenreSerializer(many=True, read_only=False)

    class Meta:
        model = Title
        fields = ("id", "name", "year", "genre", "category")


class ReviewSerializer(serializers.ModelSerializer):
    author = relations.SlugRelatedField(
        required=False, read_only=True, slug_field="username"
    )

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=["author", "title"],
                message="Пользователь может оставить только один отзыв "
                "на произведение",
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = relations.SlugRelatedField(
        required=False, read_only=True, slug_field="username"
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
