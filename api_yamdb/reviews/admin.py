from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Title


class ReviewAdmin(admin.ModelAdmin):
    ...


class CommentAdmin(admin.ModelAdmin):
    ...


class CategoryAdmin(admin.ModelAdmin):
    ...


class TitleAdmin(admin.ModelAdmin):
    ...


class GenreAdmin(admin.ModelAdmin):
    ...


class GenreTitleAdmin(admin.ModelAdmin):
    ...


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
