from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.contrib.auth.models import AbstractUser, UserManager# ← IMPORTANTE

class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 'admin')  # Ensure superusers are admins
        return super().create_superuser(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    objects = CustomUserManager()
    fullname = models.CharField(max_length=150, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

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

    @property
    def is_admin(self):
        return self.rol == 'admin'

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
        if hasattr(self, 'user') and self.user:
            return f"{self.action} - {self.module} - {self.timestamp} - {self.user.username} ({self.user.rol})"
        return f"{self.action} - {self.module} - {self.timestamp} - Usuario no disponible"



# Create your models here.
