from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AIChatView, AnalysisViewSet

router = DefaultRouter()
router.register("analyses", AnalysisViewSet, basename="analysis")

urlpatterns = [
    path("chat/", AIChatView.as_view(), name="ai-chat"),
    path("", include(router.urls)),
]