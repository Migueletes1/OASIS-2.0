from django.db import models
from django.conf import settings


class BackupJob(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        RUNNING = "running", "En proceso"
        COMPLETED = "completed", "Completado"
        FAILED = "failed", "Fallido"

    class BackupType(models.TextChoices):
        FULL = "full", "Completo"
        INCREMENTAL = "incremental", "Incremental"

    name = models.CharField(max_length=150, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    backup_type = models.CharField(
        max_length=20,
        choices=BackupType.choices,
        default=BackupType.FULL,
        verbose_name="Tipo de copia",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Estado",
    )
    file = models.FileField(
        upload_to="backups/",
        blank=True,
        null=True,
        verbose_name="Archivo generado",
    )
    log = models.TextField(blank=True, verbose_name="Registro del proceso")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_backups",
        verbose_name="Creado por",
    )
    started_at = models.DateTimeField(blank=True, null=True, verbose_name="Inicio")
    finished_at = models.DateTimeField(blank=True, null=True, verbose_name="Fin")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Copia de seguridad"
        verbose_name_plural = "Copias de seguridad"

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"
