from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Favourite, Genre, Movie


class MovieListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        drama = Genre.objects.create(code="DRA", name="Drama", description="Dramatic films.")
        comedy = Genre.objects.create(code="COM", name="Comedy", description="Comedic films.")
        sci = Genre.objects.create(code="SCI", name="Sci-Fi", description="Science fiction.")

        Movie.objects.create(
            source_code="M001", title="The Shawshank Redemption",
            genre=drama, director="Frank Darabont", year=1994,
            rating=9.3, runtime_minutes=142, description="A banker sentenced to life in Shawshank."
        )
        Movie.objects.create(
            source_code="M002", title="Groundhog Day",
            genre=comedy, director="Harold Ramis", year=1993,
            rating=8.0, runtime_minutes=101, description="A man relives the same day repeatedly."
        )
        Movie.objects.create(
            source_code="M003", title="Interstellar",
            genre=sci, director="Christopher Nolan", year=2014,
            rating=8.6, runtime_minutes=169, description="Explorers travel through a wormhole."
        )

    def test_movie_list_page_loads_and_uses_template(self):
        response = self.client.get(reverse("movie_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/movie_list.html")
        self.assertContains(response, "The Shawshank Redemption")
        self.assertContains(response, "Groundhog Day")

    def test_movie_list_shows_genre_links(self):
        response = self.client.get(reverse("movie_list"))
        self.assertContains(response, "Drama")
        self.assertContains(response, "Comedy")


class MovieDetailTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        drama = Genre.objects.create(code="DRA", name="Drama", description="Dramatic films.")
        Movie.objects.create(
            source_code="M001", title="The Shawshank Redemption",
            genre=drama, director="Frank Darabont", year=1994,
            rating=9.3, runtime_minutes=142, description="A banker sentenced to life in Shawshank."
        )

    def test_detail_page_loads_and_shows_correct_data(self):
        movie = Movie.objects.get(source_code="M001")
        response = self.client.get(reverse("movie_detail", args=[movie.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/movie_detail.html")
        self.assertContains(response, "The Shawshank Redemption")
        self.assertContains(response, "Frank Darabont")
        self.assertContains(response, "1994")

    def test_detail_page_404_for_nonexistent_movie(self):
        response = self.client.get(reverse("movie_detail", args=[99999]))
        self.assertEqual(response.status_code, 404)


class FavouritesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.genre = Genre.objects.create(code="FAV", name="Fav Genre", description="")
        cls.movie = Movie.objects.create(
            source_code="F001", title="Favourite Movie", genre=cls.genre,
            director="Test", year=2020, rating=8.0, runtime_minutes=100, description=""
        )
        cls.user = User.objects.create_user(username="testuser", password="testpass123")

    def test_favourites_page_requires_login(self):
        response = self.client.get(reverse("favourites_list"))
        self.assertRedirects(response, "/accounts/login/?next=/favourites/")

    def test_logged_in_user_can_add_favourite(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(reverse("toggle_favourite", args=[self.movie.id]))
        self.assertRedirects(response, reverse("movie_detail", args=[self.movie.id]))
        self.assertTrue(Favourite.objects.filter(user=self.user, movie=self.movie).exists())

    def test_logged_in_user_can_remove_favourite(self):
        Favourite.objects.create(user=self.user, movie=self.movie)
        self.client.login(username="testuser", password="testpass123")
        self.client.post(reverse("toggle_favourite", args=[self.movie.id]))
        self.assertFalse(Favourite.objects.filter(user=self.user, movie=self.movie).exists())

    def test_favourites_list_shows_saved_movies(self):
        Favourite.objects.create(user=self.user, movie=self.movie)
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("favourites_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Favourite Movie")

class RegistrationTests(TestCase):
    def test_register_page_loads(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_valid_registration_creates_user_and_logs_in(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "password1": "Str0ngPass!99",
            "password2": "Str0ngPass!99",
        })
        self.assertRedirects(response, reverse("movie_list"))
        self.assertTrue(User.objects.filter(username="newuser").exists())
