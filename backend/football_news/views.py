
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination

from .models import NewsArticle
from .serializers import NewsArticleSerializer


class NewsPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 50


class GlobalNewsView(generics.ListAPIView):
    serializer_class = NewsArticleSerializer
    permission_classes = [AllowAny]
    pagination_class = NewsPagination

    def get_queryset(self):
        queryset = NewsArticle.objects.all()

        category = self.request.query_params.get("category")
        search = self.request.query_params.get("search")
        source = self.request.query_params.get("source")
        rumours = self.request.query_params.get("rumours")

        if category and category != "all":
            queryset = queryset.filter(category=category)

        if search:
            queryset = queryset.filter(
                title__icontains=search
            ) | queryset.filter(
                summary__icontains=search
            )

        if source:
            queryset = queryset.filter(
                source_name__iexact=source
            )

        if rumours == "true":
            queryset = queryset.filter(is_rumour=True)

        return queryset.order_by(
            "-published_at", "-created_at"
        )
