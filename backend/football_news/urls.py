
from django.urls import path

from .views import GlobalNewsView

urlpatterns = [
    path("", GlobalNewsView.as_view(), name="global-news"),
]
