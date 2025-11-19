from django.db import models

class KnowledgeArea(models.Model):
    """
    Representa un área de conocimiento dentro del sistema OASIS.
    Puede ser usada para categorizar proyectos, aprendices,
    competencias o asignaciones.
    """

    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nombre del Área de Conocimiento"
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="¿Área activa?"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    class Meta:
        verbose_name = "Área de Conocimiento"
        verbose_name_plural = "Áreas de Conocimiento"
        ordering = ["name"]  # Orden alfabético

    def __str__(self):
        return self.name
