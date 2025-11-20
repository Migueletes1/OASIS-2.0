from django.urls import path

from . import views

app_name = "system"

urlpatterns = [
    path("", views.config_list, name="config_list"),
    path("<int:pk>/", views.config_detail, name="config_detail"),
    path("<int:pk>/edit/", views.config_edit, name="config_edit"),
]
