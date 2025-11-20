from django.urls import path

from . import views

app_name = "progress"

urlpatterns = [
    path("", views.progress_list, name="progress_list"),
    path("create/", views.progress_create, name="progress_create"),
    path("<int:pk>/", views.progress_detail, name="progress_detail"),
    path("<int:pk>/edit/", views.progress_edit, name="progress_edit"),
    path("dashboard/", views.progress_dashboard, name="progress_dashboard"),
    path("reports/", views.progress_reports, name="progress_reports"),
]
