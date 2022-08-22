from django.core.validators import RegexValidator
from rest_framework import relations, serializers, validators
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
    User,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class UserEditSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()
    role = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError(
                "me нельзя использовать в качестве username"
            )
        return value


class UserSignupConfirmSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")


class CategorySerializer(serializers.ModelSerializer):
    queryset = Category.objects.all()
    name = serializers.CharField(max_length=256)
    slug = serializers.SlugField(
        max_length=50,
        validators=[
            validators.UniqueValidator(queryset),
            RegexValidator(
                regex=r"^[-a-zA-Z0-9_]+$",
                message=("Slug должен быть буквенно-цифровым"),
            ),
        ],
    )

    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    queryset = Genre.objects.all()

    class Meta:
        model = Genre
        fields = ("name", "slug")


class ReviewSerializer(serializers.ModelSerializer):
    author = relations.SlugRelatedField(
        required=False,
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )
    title = relations.SlugRelatedField(
        required=False,
        read_only=True,
        slug_field="name",
    )

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date", "title")


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        return obj.get_rating().get("rating", 0)

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field="slug",
    )
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field="slug",
    )
    # genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )

    """def create(self, validated_data):
        genre = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for i in genre:
            current_genre, status = Genre.objects.get(id=id)
            GenreTitle.objects.create(genre=current_genre, title=title)
        return title"""


class CommentSerializer(serializers.ModelSerializer):
    author = relations.SlugRelatedField(
        required=False, read_only=True, slug_field="username"
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
