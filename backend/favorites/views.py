
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError

from .models import Favorite
from .serializers import FavoriteSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "delete", "head", "options"]

    def get_queryset(self):
        return Favorite.objects.filter(
            user=self.request.user
        ).select_related("content_type")

    def perform_create(self, serializer):
        content_type_id = self.request.data.get("content_type")
        object_id = self.request.data.get("object_id")

        try:
            content_type = ContentType.objects.get_for_id(
                int(content_type_id)
            )
            from football.models import Team, Player

            allowed_models = [Team, Player]
            if content_type.model_class() not in allowed_models:
                raise ValidationError(
                    "Only teams and players can be favorited."
                )

            model = content_type.model_class()
            get_object_or_404(model, pk=object_id)

        except (TypeError, ValueError, ContentType.DoesNotExist):
            raise ValidationError("Invalid favorite target.")

        serializer.save(
            user=self.request.user,
            content_type=content_type,
        )
