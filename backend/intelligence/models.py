
from django.conf import settings
from django.db import models


class Analysis(models.Model):
    class AnalysisType(models.TextChoices):
        MATCH = "match", "Match Analysis"
        PLAYER = "player", "Player Analysis"
        TEAM = "team", "Team Analysis"
        NEWS = "news", "Football News Analysis"
        GENERAL = "general", "General Intelligence"

    title = models.CharField(max_length=200)

    analysis_type = models.CharField(
        max_length=10,
        choices=AnalysisType.choices,
        default=AnalysisType.GENERAL,
    )

    summary = models.TextField()

    data = models.JSONField(default=dict, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="analyses",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
