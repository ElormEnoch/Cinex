from django.contrib import admin

from .models import Favourite, Genre, Movie


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "genre", "director", "year", "rating", "runtime_minutes")
    list_filter = ("genre", "year")
    search_fields = ("title", "director", "source_code")


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "added_at")
    list_filter = ("user",)
