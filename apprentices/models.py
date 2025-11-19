from django.db import models
from django.conf import settings


class Apprentice(models.Model):
    """
    Representa un aprendiz dentro del sistema OASIS.
    Puede estar asociado a un programa o a un proyecto.
    """

    # Información básica
    full_name = models.CharField(
        max_length=120,
        verbose_name="Nombre completo"
    )
    document_type_choices = [
        ("CC", "Cédula de Ciudadanía"),
        ("TI", "Tarjeta de Identidad"),
        ("CE", "Cédula de Extranjería"),
    ]

    document_type = models.CharField(
        max_length=3,
        choices=document_type_choices,
        verbose_name="Tipo de documento"
    )

    document_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Número de documento"
    )

    email = models.EmailField(
        verbose_name="Correo electrónico",
        unique=True
    )

    phone = models.CharField(
        max_length=20,
        verbose_name="Teléfono"
    )

    # Programa de formación
    program = models.CharField(
        max_length=150,
        verbose_name="Programa de formación"
    )

    # Estado del aprendiz
    status_choices = [
        ("active", "Activo"),
        ("inactive", "Inactivo"),
        ("suspended", "Suspendido"),
    ]

    status = models.CharField(
        max_length=20,
        choices=status_choices,
        default="active",
        verbose_name="Estado"
    )

    # Relación con usuario del sistema (opcional)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="apprentice_profile",
        verbose_name="Usuario vinculado"
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
        return f"{self.full_name} ({self.document_number})"

    class Meta:
        verbose_name = "Aprendiz"
        verbose_name_plural = "Aprendices"
        ordering = ["full_name"]

