from rest_framework import relations, serializers
from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', )


class ReviewSerializer(serializers.ModelSerializer):
    author = relations.SlugRelatedField(
        required=False, read_only=True, slug_field="username"
    )

    def validate_score(self):
        if not (1 <= self.score <= 10):
            raise serializers.ValidationError("Оценка должна быть ≥ 1 и ≤ 10")

    class Meta:
        model = Review
        fields = ["id", "text", "author", "score", "pub_date"]


class CommentSerializer(serializers.ModelSerializer):
    author = relations.SlugRelatedField(
        required=False, read_only=True, slug_field="username"
    )

    class Meta:
        model = Comment
        fields = ["id", "text", "author", "pub_date"]
