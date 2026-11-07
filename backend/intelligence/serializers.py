
from rest_framework import serializers
from .models import Analysis


class AnalysisSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(
        source="created_by.username",
        read_only=True,
        default=None,
    )

    class Meta:
        model = Analysis
        fields = "__all__"
        read_only_fields = [
            "id", "created_by", "created_at",
        ]
