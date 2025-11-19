from django.db import models
from django.contrib.auth.models import AbstractUser     # ← IMPORTANTE

class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=150, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.username
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cédula de ciudadanía'),
        ('TI', 'Tarjeta de identidad'),
        ('CE', 'Cédula de extranjería'),
        ('PP', 'Pasaporte'),
    ]

    tipo_documento = models.CharField(max_length=5, choices=TIPO_DOCUMENTO_CHOICES, blank=True, null=True)
    numero_documento = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    
    rol = models.CharField(
        max_length=20,
        choices=[
            ('admin', 'Administrador'),
            ('empresa', 'Empresa'),
            ('instructor', 'Instructor'),
            ('aprendiz', 'Aprendiz'),
        ],
        default='aprendiz'
    )

    estado = models.CharField(
        max_length=20,
        choices=[
            ('activo', 'Activo'),
            ('inactivo', 'Inactivo'),
        ],
        default='activo'
    )

    def __str__(self):
        return f"{self.username} ({self.rol})"


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Creación'),
        ('update', 'Actualización'),
        ('delete', 'Eliminación'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    module = models.CharField(max_length=100, default='users')
    description = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.module} - {self.timestamp}"



# Create your models here.
