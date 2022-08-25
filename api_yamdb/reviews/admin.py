from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    list_editable = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    list_editable = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "year", "category", "description")
    search_fields = (
        "name",
        "year",
        "category__name",
        "category__slug",
        "genre__name",
        "genre__slug",
    )
    list_display_links = ("pk",)


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ("pk", "genre", "title")
    list_display_links = ("pk", "genre", "title")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "text", "pub_date", "score", "author")
    list_display_links = ("pk", "title", "text", "pub_date", "score", "author")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "review", "text", "pub_date", "author")
    list_display_links = ("pk", "review", "text", "pub_date", "author")
