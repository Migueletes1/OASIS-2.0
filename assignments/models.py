from django.db import models
from django.conf import settings
from companies.models import Company
from projects.models import Project
from instructors.models import Instructor


class Assignment(models.Model):
    """
    Representa la asignación de aprendices, instructores y empresas a un proyecto.
    """

    # Proyecto asignado
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="assignments",
        verbose_name="Proyecto"
    )

    # Empresa donde se desarrolla el proyecto
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="assignments",
        verbose_name="Empresa"
    )

    # Instructor asignado
    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assignments",
        verbose_name="Instructor"
    )

    # Aprendices asignados (usuarios del sistema)
    apprentices = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="apprentice_assignments",
        blank=True,
        verbose_name="Aprendices"
    )

    # Información adicional
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )

    # Estado de la asignación
    status_choices = [
        ("active", "Activa"),
        ("finished", "Finalizada"),
        ("cancelled", "Cancelada"),
    ]

    status = models.CharField(
        max_length=20,
        choices=status_choices,
        default="active",
        verbose_name="Estado"
    )

    # Fechas
    assigned_at = models.DateField(
        auto_now_add=True,
        verbose_name="Fecha de asignación"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Registrado"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    def __str__(self):
        return f"Asignación de {self.project.title} - {self.company.name}"

    class Meta:
        verbose_name = "Asignación"
        verbose_name_plural = "Asignaciones"
        ordering = ["-created_at"]

