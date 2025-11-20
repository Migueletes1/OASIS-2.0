from django.db import models
from django.conf import settings


class ProjectAttachment(models.Model):
    class AttachmentType(models.TextChoices):
        DOCUMENT = "document", "Documento"
        IMAGE = "image", "Imagen"
        ARCHIVE = "archive", "Archivo comprimido"
        OTHER = "other", "Otro"

    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="attachments",
        verbose_name="Proyecto",
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_attachments",
        verbose_name="Subido por",
    )
    file = models.FileField(upload_to="project_attachments/", verbose_name="Archivo")
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(blank=True, verbose_name="Descripción")
    attachment_type = models.CharField(
        max_length=20,
        choices=AttachmentType.choices,
        default=AttachmentType.DOCUMENT,
        verbose_name="Tipo",
    )
    is_public = models.BooleanField(default=False, verbose_name="¿Visible para aprendices?")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Adjunto"
        verbose_name_plural = "Adjuntos"

    def __str__(self):
        return f"{self.project} - {self.title}"
