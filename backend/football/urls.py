
from rest_framework.routers import DefaultRouter
from .views import (
    CompetitionViewSet,
    TeamViewSet,
    PlayerViewSet,
    MatchViewSet,
)

router = DefaultRouter()
router.register("competitions", CompetitionViewSet)
router.register("teams", TeamViewSet)
router.register("players", PlayerViewSet)
router.register("matches", MatchViewSet)

urlpatterns = router.urls
