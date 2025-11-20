from django.db import models
from django.conf import settings


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ("create", "Creación"),
        ("update", "Actualización"),
        ("delete", "Eliminación"),
        ("login", "Inicio de sesión"),
        ("permission", "Cambio de permisos"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
        verbose_name="Usuario",
    )
    module = models.CharField(max_length=120, verbose_name="Módulo")
    action = models.CharField(max_length=30, choices=ACTION_CHOICES, verbose_name="Acción")
    description = models.TextField(verbose_name="Descripción")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Registro de auditoría"
        verbose_name_plural = "Registros de auditoría"

    def __str__(self):
        return f"[{self.module}] {self.action} - {self.created_at:%Y-%m-%d %H:%M}"
