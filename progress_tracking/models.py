from django.db import models
from django.conf import settings


class ProgressTracking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        REVIEWED = "reviewed", "Revisado"
        CORRECTION = "correction", "Corrección"

    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="progress_entries",
        verbose_name="Proyecto",
    )
    apprentice = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="progress_entries",
        verbose_name="Aprendiz",
    )
    instructor_reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="reviewed_progress_entries",
        null=True,
        blank=True,
        verbose_name="Instructor revisor",
    )
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción del avance")
    progress_percentage = models.PositiveIntegerField(
        verbose_name="Porcentaje de avance",
        default=0,
        help_text="Ingrese un valor entre 0 y 100",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Estado",
    )
    evidence_file = models.FileField(
        upload_to="progress_evidence/",
        null=True,
        blank=True,
        verbose_name="Evidencia",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Avance"
        verbose_name_plural = "Avances"

    def __str__(self):
        return f"{self.project} - {self.title} ({self.progress_percentage}%)"
