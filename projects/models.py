from django.db import models
from django.conf import settings
from companies.models import Company


class Project(models.Model):
    """
    Representa un proyecto asignado a una empresa y desarrollado por uno o varios aprendices.
    """

    # Información general del proyecto
    title = models.CharField(
        max_length=150,
        verbose_name="Título del proyecto"
    )
    description = models.TextField(
        verbose_name="Descripción"
    )
    objective = models.TextField(
        verbose_name="Objetivo general",
        blank=True,
        null=True
    )

    # Relación con empresa
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="projects",
        verbose_name="Empresa"
    )

    # Estado del proyecto
    status_choices = [
        ("pending", "Pendiente"),
        ("in_progress", "En desarrollo"),
        ("completed", "Completado"),
        ("cancelled", "Cancelado"),
    ]

    status = models.CharField(
        max_length=20,
        choices=status_choices,
        default="pending",
        verbose_name="Estado"
    )

    # Fechas
    start_date = models.DateField(
        verbose_name="Fecha de inicio"
    )
    end_date = models.DateField(
        verbose_name="Fecha de finalización",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Registrado"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    # Relación con aprendices (usuarios)
    apprentices = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="assigned_projects",
        blank=True,
        verbose_name="Aprendices asignados"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ["-created_at"]


# Create your models here.
