from django.urls import path

from . import views

urlpatterns = [
    path("", views.movie_list, name="movie_list"),
    path("movies/<int:movie_id>/", views.movie_detail, name="movie_detail"),
    path("movies/<int:movie_id>/favourite/", views.toggle_favourite, name="toggle_favourite"),
    path("favourites/", views.favourites_list, name="favourites_list"),
    path("genres/<int:genre_id>/", views.genre_detail, name="genre_detail"),
]
