from django.urls import path

from . import views

app_name = "evaluations"

urlpatterns = [
    path("", views.evaluation_list, name="evaluation_list"),
    path("create/", views.evaluation_create, name="evaluation_create"),
    path("<int:pk>/", views.evaluation_detail, name="evaluation_detail"),
    path("<int:pk>/edit/", views.evaluation_edit, name="evaluation_edit"),
    path("dashboard/", views.evaluation_dashboard, name="evaluation_dashboard"),
    path("reports/", views.evaluation_report, name="evaluation_report"),
]
