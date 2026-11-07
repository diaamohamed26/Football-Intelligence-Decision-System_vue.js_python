
from rest_framework import serializers

from .models import NewsArticle


class NewsArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsArticle
        fields = [
            "id",
            "title",
            "summary",
            "source_name",
            "source_url",
            "article_url",
            "image_url",
            "category",
            "is_rumour",
            "published_at",
        ]
