from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("", views.report_dashboard, name="report_dashboard"),
    path("projects/", views.report_projects, name="report_projects"),
    path("assignments/", views.report_assignments, name="report_assignments"),
    path("programs/", views.report_programs, name="report_programs"),
    path("export/", views.report_export, name="report_export"),
]
