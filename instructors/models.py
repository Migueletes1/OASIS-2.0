from django.db import models
from django.conf import settings
from knowledge_areas.models import KnowledgeArea


class Instructor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    specialty = models.CharField(max_length=150)
    avatar = models.ImageField(upload_to="instructors/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="instructor_profile"
    )

    full_name = models.CharField(max_length=150)
    document_number = models.CharField(max_length=50, unique=True)

    # Especialidad técnica o área que maneja
    specialty = models.CharField(max_length=120)

    # Relación con áreas de conocimiento del sistema OASIS
    knowledge_area = models.ForeignKey(
        KnowledgeArea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="instructors"
    )

    # Disponibilidad
    availability = models.CharField(
        max_length=200,
        help_text="Ejemplo: Lunes a Viernes 8am - 12pm"
    )

    # Información adicional
    phone = models.CharField(max_length=20, blank=True)
    professional_title = models.CharField(max_length=150, blank=True)
    experience_years = models.PositiveIntegerField(default=0)

    # Estado
    is_active = models.BooleanField(default=True)

    # Fecha de creación
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["full_name"]
        verbose_name = "Instructor"
        verbose_name_plural = "Instructores"

    def __str__(self):
        return self.full_name

