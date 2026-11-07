
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db import transaction
from football.models import Team, Competition

competitions = [
    ("Premier League", "England"),
    ("La Liga", "Spain"),
    ("UEFA Champions League", "Europe"),
    ("Bundesliga", "Germany"),
    ("Serie A", "Italy"),
]

teams = [
    ("Arsenal", "ARS", "England", 1886),
    ("Liverpool", "LIV", "England", 1892),
    ("Manchester City", "MCI", "England", 1880),
    ("Manchester United", "MUN", "England", 1878),
    ("Chelsea", "CHE", "England", 1905),
    ("Tottenham Hotspur", "TOT", "England", 1882),
    ("Newcastle United", "NEW", "England", 1892),
    ("Real Madrid", "RMA", "Spain", 1902),
    ("Barcelona", "BAR", "Spain", 1899),
    ("Atletico Madrid", "ATM", "Spain", 1903),
    ("Bayern Munich", "BAY", "Germany", 1900),
    ("Borussia Dortmund", "BVB", "Germany", 1909),
    ("Bayer Leverkusen", "LEV", "Germany", 1904),
    ("Paris Saint-Germain", "PSG", "France", 1970),
    ("Marseille", "MAR", "France", 1899),
    ("Inter Milan", "INT", "Italy", 1908),
    ("AC Milan", "MIL", "Italy", 1899),
    ("Juventus", "JUV", "Italy", 1897),
    ("Napoli", "NAP", "Italy", 1926),
    ("Al Ahly", "AHL", "Egypt", 1907),
]

with transaction.atomic():
    for name, country in competitions:
        Competition.objects.update_or_create(
            name=name,
            season="2026/2027",
            defaults={
                "country": country,
                "logo": "",
            },
        )

    for name, short_name, country, founded in teams:
        Team.objects.update_or_create(
            name=name,
            defaults={
                "short_name": short_name,
                "country": country,
                "founded": founded,
                "logo": "",
            },
        )

print("FIDS DATABASE SEEDED SUCCESSFULLY")
print("Competitions:", Competition.objects.count())
print("Teams:", Team.objects.count())
