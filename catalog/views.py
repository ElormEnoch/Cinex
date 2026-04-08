from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Favourite, Genre, Movie


def movie_list(request):
    """
    Public list of all movies with optional search by title or director
    and optional filtering by genre. Results are paginated at 10 per page.
    """
    search_query = request.GET.get("search", "").strip()
    genre_filter = request.GET.get("genre", "").strip()

    movies = Movie.objects.select_related("genre").all()

    if search_query:
        movies = movies.filter(
            Q(title__icontains=search_query) | Q(director__icontains=search_query)
        )

    if genre_filter:
        movies = movies.filter(genre__code=genre_filter)

    paginator = Paginator(movies, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    genres = Genre.objects.all()

    context = {
        "movies": page_obj.object_list,
        "page_obj": page_obj,
        "search_query": search_query,
        "genre_filter": genre_filter,
        "genres": genres,
    }
    return render(request, "catalog/movie_list.html", context)


def movie_detail(request, movie_id):
    """
    Detail page for a single movie. Shows all fields and, for logged-in
    users, whether the movie is already in their favourites.
    """
    movie = get_object_or_404(Movie.objects.select_related("genre"), pk=movie_id)

    is_favourite = False
    if request.user.is_authenticated:
        is_favourite = Favourite.objects.filter(
            user=request.user, movie=movie
        ).exists()

    context = {
        "movie": movie,
        "is_favourite": is_favourite,
    }
    return render(request, "catalog/movie_detail.html", context)


@login_required
def toggle_favourite(request, movie_id):
    """
    Add or remove a movie from the current user's favourites list.
    Only responds to POST requests to prevent accidental changes via links.
    Redirects back to the movie detail page with a feedback message.
    """
    if request.method != "POST":
        return redirect("movie_detail", movie_id=movie_id)

    movie = get_object_or_404(Movie, pk=movie_id)
    favourite, created = Favourite.objects.get_or_create(
        user=request.user, movie=movie
    )
    if not created:
        favourite.delete()
        messages.success(request, f'"{movie.title}" removed from your favourites.')
    else:
        messages.success(request, f'"{movie.title}" added to your favourites.')

    return redirect("movie_detail", movie_id=movie_id)


@login_required
def favourites_list(request):
    """
    Shows all movies the logged-in user has saved as favourites,
    ordered most recently added first.
    """
    favourites = (
        Favourite.objects
        .filter(user=request.user)
        .select_related("movie__genre")
    )
    return render(request, "catalog/favourites_list.html", {"favourites": favourites})


def genre_detail(request, genre_id):
    """
    Shows all movies that belong to a specific genre, with pagination.
    """
    genre = get_object_or_404(Genre, pk=genre_id)
    movies = Movie.objects.filter(genre=genre)
    paginator = Paginator(movies, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "catalog/genre_detail.html", {
        "genre": genre,
        "movies": page_obj.object_list,
        "page_obj": page_obj,
    })
