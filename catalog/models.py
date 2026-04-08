from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    """
    A film genre such as Drama, Comedy, or Thriller.
    Each genre has a short code used in the CSV dataset and a human-readable
    name with an optional description that explains the genre's characteristics.
    """
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "genres"

    def __str__(self):
        return self.name


class Movie(models.Model):
    """
    A single film entry imported from the open dataset.
    Each movie belongs to one primary genre and carries metadata such as
    director, year, rating, and a short description. The source_code field
    preserves the original dataset identifier so re-imports are idempotent.
    """
    source_code = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name="movies"
    )
    director = models.CharField(max_length=150, blank=True)
    year = models.PositiveSmallIntegerField()
    rating = models.DecimalField(
        max_digits=3, decimal_places=1,
        help_text="IMDb-style rating between 0.0 and 10.0"
    )
    runtime_minutes = models.PositiveSmallIntegerField(default=0)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} ({self.year})"


class Favourite(models.Model):
    """
    Records a logged-in user's favourite movie.
    The unique_together constraint ensures a user can favourite each movie
    at most once, preventing duplicate entries without extra application logic.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favourites"
    )
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="favourited_by"
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "movie")
        ordering = ["-added_at"]

    def __str__(self):
        return f"{self.user.username} → {self.movie.title}"
