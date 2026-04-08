from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    """
    Extends Django's built-in UserCreationForm with an optional email field.
    Validation is handled by the parent class which checks that passwords match
    and that the chosen username does not already exist.
    """
    email = forms.EmailField(required=False, help_text="Optional.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
