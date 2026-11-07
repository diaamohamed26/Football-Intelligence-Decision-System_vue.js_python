from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from accounts.dashboard_views import AdminDashboardView


def home(request):
    return JsonResponse({
        "name": "FIDS API",
        "status": "running",
        "version": "1.0",
        "health": "/api/v1/health/",
    })


def health_check(request):
    return JsonResponse({
        "status": "healthy",
        "service": "FIDS Backend",
    })




urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),

    path("api/v1/health/", health_check, name="health"),
    path("api/v1/auth/", include("accounts.urls")),
    path("api/v1/", include("football.urls")),
    path("api/v1/intelligence/", include("intelligence.urls")),
    path("api/v1/favorites/", include("favorites.urls")),
    path(
    "api/v1/admin/dashboard/",
    AdminDashboardView.as_view(),
    name="admin-dashboard",),
    path(
    "api/v1/news/",
    include("football_news.urls")
    ),
    path(
    "api/v1/intelligence/",
    include("intelligence.urls"),
    ),
    path("api/v1/ai/", include("intelligence.urls")),  
]
