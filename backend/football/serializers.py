
from rest_framework import serializers
from .models import Competition, Team, Player, Match


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class PlayerSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(
        source="team.name", read_only=True, default=None
    )

    class Meta:
        model = Player
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class MatchSerializer(serializers.ModelSerializer):
    home_team_name = serializers.CharField(
        source="home_team.name", read_only=True
    )
    away_team_name = serializers.CharField(
        source="away_team.name", read_only=True
    )
    competition_name = serializers.CharField(
        source="competition.name", read_only=True, default=None
    )

    class Meta:
        model = Match
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        home = attrs.get(
            "home_team",
            getattr(self.instance, "home_team", None),
        )
        away = attrs.get(
            "away_team",
            getattr(self.instance, "away_team", None),
        )

        if home and away and home == away:
            raise serializers.ValidationError(
                "A team cannot play against itself."
            )

        return attrs
