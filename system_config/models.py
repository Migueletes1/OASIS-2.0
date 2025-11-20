from django.db import models


class SystemSetting(models.Model):
    key = models.CharField(max_length=120, unique=True, verbose_name="Clave")
    value = models.TextField(verbose_name="Valor")
    description = models.TextField(blank=True, verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name="¿Activo?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["key"]
        verbose_name = "Configuración del sistema"
        verbose_name_plural = "Configuraciones del sistema"

    def __str__(self):
        return self.key
