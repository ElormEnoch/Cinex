import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from catalog.models import Genre, Movie


class Command(BaseCommand):
    help = "Import genres and movies from the offline CSV datasets."

    def handle(self, *args, **options):
        data_dir = Path(__file__).resolve().parents[3] / "data"
        genres_path = data_dir / "genres.csv"
        movies_path = data_dir / "movies.csv"

        genres_created = 0
        genres_updated = 0
        imported = 0
        updated = 0

        with genres_path.open(newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                _, created = Genre.objects.update_or_create(
                    code=row["code"],
                    defaults={
                        "name": row["name"],
                        "description": row["description"],
                    },
                )
                if created:
                    genres_created += 1
                else:
                    genres_updated += 1

        with movies_path.open(newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                genre = Genre.objects.get(code=row["genre_code"])
                _, created = Movie.objects.update_or_create(
                    source_code=row["source_code"],
                    defaults={
                        "title": row["title"],
                        "genre": genre,
                        "director": row["director"],
                        "year": int(row["year"]),
                        "rating": row["rating"],
                        "runtime_minutes": int(row["runtime_minutes"]),
                        "description": row["description"],
                    },
                )
                if created:
                    imported += 1
                else:
                    updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Import complete: "
                f"{genres_created} genres created, "
                f"{genres_updated} genres updated, "
                f"{imported} movies created, "
                f"{updated} movies updated."
            )
        )
