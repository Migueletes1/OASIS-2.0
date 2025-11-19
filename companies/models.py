from django.db import models


# Lista de sectores (puedes agregar más)
SECTOR_CHOICES = [
    ("Tecnología", "Tecnología"),
    ("Servicios", "Servicios"),
    ("Salud", "Salud"),
    ("Manufactura", "Manufactura"),
    ("Educación", "Educación"),
    ("Comercio", "Comercio"),
    ("Transporte", "Transporte"),
    ("Construcción", "Construcción"),
    ("Otro", "Otro"),
]


def company_logo_upload_path(instance, filename):
    """Define la ruta donde se guardará el logo."""
    return f"companies/logos/{instance.name}/{filename}"


class Company(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Nombre de la Empresa"
    )

    nit = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="NIT"
    )

    email = models.EmailField(
        unique=True,
        verbose_name="Correo de Contacto"
    )

    phone = models.CharField(
        max_length=20,
        verbose_name="Teléfono",
        blank=True,
        null=True
    )

    address = models.CharField(
        max_length=200,
        verbose_name="Dirección",
        blank=True,
        null=True
    )

    sector = models.CharField(
        max_length=50,
        choices=SECTOR_CHOICES,
        default="Tecnología",
        verbose_name="Sector Empresarial"
    )

    website = models.URLField(
        max_length=255,
        verbose_name="Sitio Web",
        blank=True,
        null=True
    )

    description = models.TextField(
        verbose_name="Descripción de la empresa",
        blank=True,
        null=True
    )

    logo = models.ImageField(
        upload_to=company_logo_upload_path,
        verbose_name="Logo",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Registro"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización"
    )

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.nit})"



# Create your models here.
