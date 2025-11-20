from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import BackupJobForm
from .models import BackupJob


@login_required
def backup_list(request):
    backups = BackupJob.objects.select_related("created_by").order_by("-created_at")
    stats = {
        "total": backups.count(),
        "completed": backups.filter(status=BackupJob.Status.COMPLETED).count(),
        "failed": backups.filter(status=BackupJob.Status.FAILED).count(),
    }
    return render(request, "backup_list.html", {"backups": backups, "stats": stats})


@login_required
def backup_create(request):
    if request.method == "POST":
        form = BackupJobForm(request.POST)
        if form.is_valid():
            backup = form.save(commit=False)
            backup.status = BackupJob.Status.RUNNING
            backup.created_by = request.user
            backup.started_at = timezone.now()
            backup.save()

            backup.finished_at = timezone.now()
            backup.status = BackupJob.Status.COMPLETED
            backup.log = "Backup ejecutado manualmente."
            backup.save(update_fields=["finished_at", "status", "log"])

            messages.success(request, "Copia de seguridad creada correctamente.")
            return redirect("backup:backup_detail", pk=backup.pk)
    else:
        form = BackupJobForm()

    return render(request, "backup_create.html", {"form": form})


@login_required
def backup_detail(request, pk):
    backup = get_object_or_404(BackupJob, pk=pk)
    return render(request, "backup_detail.html", {"backup": backup})


@login_required
def backup_restore(request, pk):
    backup = get_object_or_404(BackupJob, pk=pk)

    if request.method == "POST":
        backup.log += f"\nRestauración solicitada por {request.user} ({timezone.now()})"
        backup.status = BackupJob.Status.RUNNING
        backup.save(update_fields=["log", "status"])

        backup.status = BackupJob.Status.COMPLETED
        backup.finished_at = timezone.now()
        backup.save(update_fields=["status", "finished_at"])

        messages.success(request, "Restauración ejecutada correctamente (simulada).")
        return redirect("backup:backup_detail", pk=pk)

    return render(request, "backup_restore.html", {"backup": backup})
