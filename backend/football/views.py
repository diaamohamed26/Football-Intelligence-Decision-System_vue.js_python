
from rest_framework import viewsets, permissions
from accounts.permissions import IsAdminRole
from .models import Competition, Team, Player, Match
from .serializers import (
    CompetitionSerializer,
    TeamSerializer,
    PlayerSerializer,
    MatchSerializer,
)


class AdminWriteViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsAdminRole]

        return [permission() for permission in permission_classes]


class CompetitionViewSet(AdminWriteViewSet):
    queryset = Competition.objects.all().order_by("name")
    serializer_class = CompetitionSerializer


class TeamViewSet(AdminWriteViewSet):
    queryset = Team.objects.all().order_by("name")
    serializer_class = TeamSerializer


class PlayerViewSet(AdminWriteViewSet):
    queryset = Player.objects.select_related("team").all().order_by("name")
    serializer_class = PlayerSerializer


class MatchViewSet(AdminWriteViewSet):
    queryset = Match.objects.select_related(
        "home_team", "away_team", "competition"
    ).all().order_by("kickoff")
    serializer_class = MatchSerializer
