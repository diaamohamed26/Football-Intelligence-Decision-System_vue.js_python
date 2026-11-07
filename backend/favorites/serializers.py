
from rest_framework import serializers
from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    content_type_name = serializers.CharField(
        source="content_type.model",
        read_only=True,
    )

    class Meta:
        model = Favorite
        fields = [
            "id", "content_type", "content_type_name",
            "object_id", "created_at",
        ]
        read_only_fields = ["id", "created_at"]
