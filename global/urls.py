from django.urls import path

from . import views

app_name = "global"

urlpatterns = [
    path("", views.landing_page, name="landing"),
    path("search/", views.search_results, name="search_results"),
]
