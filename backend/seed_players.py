import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")

sys.path.insert(0, BACKEND_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from football.models import Player, Team

players = [
    {"name": "Kylian Mbappe", "team": "Real Madrid", "position": "FW", "nationality": "France", "age": 27},
    {"name": "Vinicius Junior", "team": "Real Madrid", "position": "FW", "nationality": "Brazil", "age": 26},
    {"name": "Jude Bellingham", "team": "Real Madrid", "position": "MF", "nationality": "England", "age": 23},
    {"name": "Erling Haaland", "team": "Manchester City", "position": "FW", "nationality": "Norway", "age": 26},
    {"name": "Phil Foden", "team": "Manchester City", "position": "MF", "nationality": "England", "age": 26},
    {"name": "Lamine Yamal", "team": "Barcelona", "position": "FW", "nationality": "Spain", "age": 19},
    {"name": "Pedri", "team": "Barcelona", "position": "MF", "nationality": "Spain", "age": 23},
    {"name": "Harry Kane", "team": "Bayern Munich", "position": "FW", "nationality": "England", "age": 33},
    {"name": "Mohamed Salah", "team": "Liverpool", "position": "FW", "nationality": "Egypt", "age": 34},
    {"name": "Bukayo Saka", "team": "Arsenal", "position": "FW", "nationality": "England", "age": 25},
]

for data in players:
    team = Team.objects.filter(name__iexact=data["team"]).first()

    if not team:
        print(f"Skipped {data['name']}: team not found ({data['team']})")
        continue

    player_data = data.copy()
    player_data.pop("team")

    Player.objects.update_or_create(
        name=data["name"],
        defaults={**player_data, "team": team},
    )

    print(f"Saved: {data['name']}")

print("Player seeding completed!")