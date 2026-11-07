
from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from football.models import Match
from intelligence.models import Analysis


User = get_user_model()


class AdminDashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        total_matches = Match.objects.count()
        total_analyses = Analysis.objects.count()

        recent_users = User.objects.order_by("-date_joined")[:5]

        return Response({
            "stats": {
                "total_users": total_users,
                "active_users": active_users,
                "total_matches": total_matches,
                "total_analyses": total_analyses,
                "total_teams": self._count("football", "Team"),
                "total_players": self._count("football", "Player"),
                "total_competitions": self._count(
                    "football", "Competition"
                ),
            },
            "recent_users": [
                {
                    "id": user.id,
                    "username": user.username,
                    "name": user.get_full_name() or user.username,
                    "email": user.email,
                    "role": user.role,
                    "is_active": user.is_active,
                    "date_joined": user.date_joined,
                }
                for user in recent_users
            ],
        })

    @staticmethod
    def _count(app_label, model_name):
        from django.apps import apps

        model = apps.get_model(app_label, model_name)
        return model.objects.count()
