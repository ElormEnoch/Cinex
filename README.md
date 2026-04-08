# MovieSite

A simple Django movie catalog web application with user authentication, genre browsing, and favourite movie tracking.

## Features

- Browse movies by title, director, or genre
- View detailed movie pages
- Register, log in, and log out
- Save movies to a personal favourites list
- Import movie and genre data from local CSV files
- Pagination with a maximum of 15 items per page

## Requirements

- Python 3.11+ (or compatible Python 3.x)
- Django 5.2.12

## Setup

   ```bash
python -m venv .venv
source .venv\Scripts\Activate.ps1      # PowerShell
source .venv\Scripts\activate.bat      # Command Prompt
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py import_movies
python manage.py test
```

## Run the application

```bash
python manage.py runserver
```

Then open `http://127.0.0.1:8000/` in your browser.

## URL reference

- Home / movie list: `/`
- Movie detail: `/movies/<movie_id>/`
- Genre detail: `/genres/<genre_id>/`
- My favourites: `/favourites/`
- Register: `/accounts/register/`
- Login: `/accounts/login/`
- Logout: `/accounts/logout/`

## Application structure

- `accounts/` — user registration and authentication
- `catalog/` — movie and genre models, views, and templates
- `data/` — source CSV files used by the import command
- `moviesite/` — main Django project settings and URL configuration

## Notes
- The list page shows 15 movies at a time
- The `Previous` and `Next` link move between pages
- Every movie belongs to a genre.
- The logout action is implemented as a POST form to support Django's logout flow.
- Use the CSV import command again after updating `data/movies.csv` or `data/genres.csv`.
