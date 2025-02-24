import json
from django.core.management.base import BaseCommand
from planetarium.models import ShowTheme, PlanetariumDome, AstronomyShow, ShowSession


class Command(BaseCommand):
    help = "Завантажує стартові дані в базу"

    def handle(self, *args, **kwargs):
        with open("seed_data.json", encoding="utf-8") as f:
            data = json.load(f)

            for theme in data.get("showtheme", []):
                ShowTheme.objects.get_or_create(name=theme["name"])

            for dome in data.get("planetariumdome", []):
                PlanetariumDome.objects.get_or_create(name=dome["name"], capacity=dome["capacity"])

            for show in data.get("astronomyshow", []):
                AstronomyShow.objects.get_or_create(
                    title=show["title"],
                    duration=show["duration"],
                    theme_id=show["theme_id"]
                )

            for session in data.get("showsession", []):
                ShowSession.objects.get_or_create(
                    show_id=session["show_id"],
                    dome_id=session["dome_id"],
                    start_time=session["start_time"]
                )

        self.stdout.write(self.style.SUCCESS("✅ Дані успішно завантажені!"))
