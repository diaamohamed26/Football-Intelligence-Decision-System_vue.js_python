
from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Competition(TimestampedModel):
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=100, blank=True)
    logo = models.URLField(blank=True)
    season = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name


class Team(TimestampedModel):
    name = models.CharField(max_length=150)
    short_name = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=100, blank=True)
    logo = models.URLField(blank=True)
    founded = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Player(TimestampedModel):
    class Position(models.TextChoices):
        GOALKEEPER = "GK", "Goalkeeper"
        DEFENDER = "DF", "Defender"
        MIDFIELDER = "MF", "Midfielder"
        FORWARD = "FW", "Forward"

    name = models.CharField(max_length=150)
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="players",
    )
    position = models.CharField(
        max_length=2,
        choices=Position.choices,
        blank=True,
    )
    nationality = models.CharField(max_length=100, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    photo = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Match(TimestampedModel):
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        LIVE = "live", "Live"
        FINISHED = "finished", "Finished"
        POSTPONED = "postponed", "Postponed"

    competition = models.ForeignKey(
        Competition,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="matches",
    )
    home_team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name="home_matches",
    )
    away_team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name="away_matches",
    )
    kickoff = models.DateTimeField()
    home_score = models.PositiveSmallIntegerField(null=True, blank=True)
    away_score = models.PositiveSmallIntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.SCHEDULED,
    )

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"
