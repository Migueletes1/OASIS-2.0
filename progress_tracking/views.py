from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Max, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProgressTrackingForm
from .models import ProgressTracking


@login_required
def progress_list(request):
    """Listado general de avances."""

    queryset = ProgressTracking.objects.select_related("project", "apprentice")

    # Los aprendices solo ven sus registros.
    if getattr(request.user, "rol", None) == "aprendiz":
        queryset = queryset.filter(apprentice=request.user)

    # Instructores ven avances que revisan.
    if getattr(request.user, "rol", None) == "instructor":
        queryset = queryset.filter(
            Q(instructor_reviewer=request.user) | Q(apprentice=request.user)
        )

    context = {
        "progress_entries": queryset.order_by("-created_at"),
    }
    return render(request, "progress_list.html", context)


@login_required
def progress_detail(request, pk):
    """Detalle de un avance específico."""

    progress = get_object_or_404(ProgressTracking, pk=pk)

    # Permisos básicos
    if request.user not in {progress.apprentice, progress.instructor_reviewer} and not request.user.is_staff:
        messages.error(request, "No tienes permisos para ver este avance.")
        return redirect("progress:progress_list")

    return render(request, "progress_detail.html", {"progress": progress})


@login_required
def progress_create(request):
    """Registro de un nuevo avance por parte del aprendiz."""

    if request.method == "POST":
        form = ProgressTrackingForm(request.POST, request.FILES)
        if form.is_valid():
            progress = form.save(commit=False)
            if getattr(request.user, "rol", None) == "aprendiz":
                progress.apprentice = request.user
            progress.save()
            form.save_m2m()
            messages.success(request, "Avance registrado correctamente.")
            return redirect("progress:progress_detail", pk=progress.pk)
    else:
        form = ProgressTrackingForm(initial={"apprentice": request.user})

    return render(request, "progress_create.html", {"form": form})


@login_required
def progress_edit(request, pk):
    """Permite editar un avance (aprendiz o instructor revisor)."""

    progress = get_object_or_404(ProgressTracking, pk=pk)
    if request.user not in {progress.apprentice, progress.instructor_reviewer} and not request.user.is_staff:
        messages.error(request, "No tienes permisos para editar este avance.")
        return redirect("progress:progress_detail", pk=pk)

    if request.method == "POST":
        form = ProgressTrackingForm(request.POST, request.FILES, instance=progress)
        if form.is_valid():
            form.save()
            messages.success(request, "Avance actualizado correctamente.")
            return redirect("progress:progress_detail", pk=pk)
    else:
        form = ProgressTrackingForm(instance=progress)

    return render(request, "progress_edit.html", {"form": form, "progress": progress})


@login_required
def progress_dashboard(request):
    """Dashboard con métricas generales de avances."""

    total = ProgressTracking.objects.count()
    context = {
        "totals": {
            "total": total,
            "pending": ProgressTracking.objects.filter(status=ProgressTracking.Status.PENDING).count(),
            "reviewed": ProgressTracking.objects.filter(status=ProgressTracking.Status.REVIEWED).count(),
            "correction": ProgressTracking.objects.filter(status=ProgressTracking.Status.CORRECTION).count(),
        },
        "project_progress": ProgressTracking.objects.values(
            "project__id", "project__title"
        ).annotate(
            entries=Count("id"),
            average_progress=Avg("progress_percentage"),
            last_update=Max("updated_at"),
        ).order_by("-average_progress"),
    }

    return render(request, "progress_dashboard.html", context)


@login_required
def progress_reports(request):
    """Reportes agregados por proyecto y estado."""

    project_summary = (
        ProgressTracking.objects.values("project__title")
        .annotate(
            entries=Count("id"),
            avg_progress=Avg("progress_percentage"),
            pending=Count("id", filter=Q(status=ProgressTracking.Status.PENDING)),
            reviewed=Count("id", filter=Q(status=ProgressTracking.Status.REVIEWED)),
            correction=Count("id", filter=Q(status=ProgressTracking.Status.CORRECTION)),
        )
        .order_by("project__title")
    )

    context = {
        "project_summary": project_summary,
    }
    return render(request, "progress_reports.html", context)
