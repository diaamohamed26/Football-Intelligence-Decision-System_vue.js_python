
from django.db import models


class NewsArticle(models.Model):

    class Category(models.TextChoices):
        BREAKING = "breaking", "Breaking News"
        TRANSFERS = "transfers", "Transfers"
        MATCHES = "matches", "Match News"
        INJURIES = "injuries", "Injuries"
        MANAGERS = "managers", "Managers"
        INTERNATIONAL = "international", "International"
        GENERAL = "general", "General"

    title = models.CharField(max_length=500)
    summary = models.TextField(blank=True)

    source_name = models.CharField(max_length=150)
    source_url = models.URLField(max_length=1000)
    article_url = models.URLField(max_length=1000, unique=True)

    image_url = models.URLField(blank=True)

    category = models.CharField(
        max_length=30,
        choices=Category.choices,
        default=Category.GENERAL
    )

    is_rumour = models.BooleanField(default=False)

    published_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title
