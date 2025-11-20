from django.db import models
from django.conf import settings


class Notification(models.Model):
    class Type(models.TextChoices):
        INFO = "info", "Información"
        WARNING = "warning", "Advertencia"
        SUCCESS = "success", "Éxito"
        ERROR = "error", "Error"

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="Destinatario",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="sent_notifications",
        verbose_name="Remitente",
        null=True,
        blank=True,
    )
    message = models.TextField(verbose_name="Mensaje")
    type = models.CharField(
        max_length=20,
        choices=Type.choices,
        default=Type.INFO,
        verbose_name="Tipo",
    )
    is_read = models.BooleanField(default=False, verbose_name="¿Leída?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"

    def __str__(self):
        return f"{self.get_type_display()} - {self.message[:30]}"
