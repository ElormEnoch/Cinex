from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import RegistrationForm


def register(request):
    """
    Handles new user registration. On a valid POST the user is created,
    immediately logged in, and redirected to the movie list. Errors are
    displayed inline within the form.
    """
    if request.user.is_authenticated:
        return redirect("movie_list")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect("movie_list")
    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})
