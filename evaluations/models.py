from django.db import models
from django.conf import settings


class Evaluation(models.Model):
    """Evaluaciones de desempeño para aprendices y proyectos."""

    STATUS_CHOICES = [
        ("pending", "Pendiente"),
        ("completed", "Completada"),
        ("approved", "Aprobada"),
        ("rejected", "Rechazada"),
    ]

    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="evaluations",
        verbose_name="Proyecto",
    )
    apprentice = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="evaluations",
        verbose_name="Aprendiz",
    )
    evaluator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="given_evaluations",
        verbose_name="Evaluador",
        null=True,
        blank=True,
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="Puntaje",
        help_text="Valor numérico de 1 a 100",
    )
    observations = models.TextField(
        verbose_name="Observaciones",
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="Estado",
    )
    report_file = models.FileField(
        upload_to="evaluation_reports/",
        null=True,
        blank=True,
        verbose_name="Adjunto",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Evaluación"
        verbose_name_plural = "Evaluaciones"

    def __str__(self):
        return f"Evaluación {self.project} - {self.apprentice} ({self.score})"
