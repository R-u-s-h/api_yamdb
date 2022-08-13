from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Категория",
        help_text="Введите название категории",
    )
    slug = models.SlugField(
        unique=True,
        help_text="Задайте slug",
    )

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Жанр",
        help_text="Введите название жанра",
    )
    slug = models.SlugField(
        unique=True,
        help_text="Задайте slug",
    )

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Title(models.Model):
    name = models.TextField(
        verbose_name="Название произведения",
        help_text="Введите название произведения",
    )
    year = models.IntegerField(
        validators=[
            # Древнейшие:
            # - книга — "Эпос о Гильгамеше", ~2200 г. до н.э.
            # - муз. произведение — Гимн богине Никкал, ~1400 г. до н.э.
            MinValueValidator(-2500),
            MaxValueValidator(2050),
        ],
        verbose_name="Год выпуска",
        help_text="Укажите год выпуска",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="titles",
        verbose_name="Категория",
        help_text="Укажите категорию",
    )
    genre = models.ManyToManyField(
        Genre,
        through="GenreTitle",
        verbose_name="Жанр",
        help_text="Укажите жанр",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Название произведения"
        verbose_name_plural = "Названия произведений"


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name="Жанр",
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="Название произведения",
    )

    def __str__(self):
        return f"{self.genre} {self.title}"


class Review(models.Model):
    text = models.TextField(
        verbose_name="Текст отзыва",
        help_text="Напишите отзыв",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время публикации отзыва",
        help_text="Дата и время публикации отзыва (автоматическое поле)",
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
        verbose_name="Оценка",
        help_text="Поставьте оценку",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор отзыва",
        help_text="Автор отзыва (автоматическое поле)",
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="Произведение",
        help_text="Произведение",
    )

    def __str__(self):
        return self.text[:25]

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="author_title"
            )
        ]


class Comment(models.Model):
    text = models.TextField(
        verbose_name="Текст комментария",
        help_text="Напишите комментарий",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время публикации комментария",
        help_text="Дата и время публикации комментария (автоматическое поле)",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария",
        help_text="Автор комментария (автоматическое поле)",
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name="Отзыв",
        help_text="Укажите комментируемый отзыв",
    )

    def __str__(self):
        return self.text[:25]

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
