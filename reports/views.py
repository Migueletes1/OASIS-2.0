import csv
from datetime import datetime

from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.http import HttpResponse
from django.shortcuts import render

from assignments.models import Assignment
from progress_tracking.models import ProgressTracking
from projects.models import Project


def _get_program_queryset():
    try:
        Program = apps.get_model("programs", "Program")
    except LookupError:
        return []
    return Program.objects.all()


@login_required
def report_dashboard(request):
    context = {
        "project_stats": {
            "total": Project.objects.count(),
            "active": Project.objects.filter(status="in_progress").count(),
            "completed": Project.objects.filter(status="completed").count(),
        },
        "assignment_stats": {
            "total": Assignment.objects.count(),
            "active": Assignment.objects.filter(status="active").count(),
        },
        "progress_stats": ProgressTracking.objects.aggregate(
            avg_progress=Avg("progress_percentage"), count=Count("id")
        ),
    }
    return render(request, "report_dashboard.html", context)


@login_required
def report_projects(request):
    status = request.GET.get("status")
    projects = Project.objects.select_related("company")
    if status:
        projects = projects.filter(status=status)

    context = {
        "projects": projects.order_by("-created_at"),
        "status_filter": status,
    }
    return render(request, "report_projects.html", context)


@login_required
def report_assignments(request):
    assignments = (
        Assignment.objects.select_related("project", "company", "instructor")
        .prefetch_related("apprentices")
        .order_by("-created_at")
    )
    stats = assignments.aggregate(
        total=Count("id"),
        active=Count("id", filter=Q(status="active")),
        finished=Count("id", filter=Q(status="finished")),
    )

    context = {
        "assignments": assignments,
        "stats": stats,
    }
    return render(request, "report_assignments.html", context)


@login_required
def report_programs(request):
    programs = _get_program_queryset()
    context = {
        "programs": programs,
        "count": len(programs) if isinstance(programs, list) else programs.count(),
    }
    return render(request, "report_programs.html", context)


@login_required
def report_export(request):
    response = HttpResponse(content_type="text/csv")
    filename = f"projects_report_{datetime.now():%Y%m%d_%H%M%S}.csv"
    response["Content-Disposition"] = f"attachment; filename={filename}"

    writer = csv.writer(response)
    writer.writerow(["Título", "Empresa", "Estado", "Fecha creación"])
    for project in Project.objects.select_related("company").order_by("-created_at"):
        writer.writerow([
            project.title,
            project.company.name,
            project.get_status_display() if hasattr(project, "get_status_display") else project.status,
            project.created_at.strftime("%Y-%m-%d"),
        ])

    return response
