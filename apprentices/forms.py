from django import forms
from .models import Apprentice


class ApprenticeForm(forms.ModelForm):
    """
    Formulario para crear y editar aprendices.
    """

    class Meta:
        model = Apprentice
        fields = [
            "full_name",
            "document_type",
            "document_number",
            "email",
            "phone",
            "program",
            "status",
            "user",
        ]

        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre completo"
            }),
            "document_type": forms.Select(attrs={
                "class": "form-control"
            }),
            "document_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Número de documento"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Correo electrónico"
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Teléfono"
            }),
            "program": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Programa de formación"
            }),
            "status": forms.Select(attrs={
                "class": "form-control"
            }),
            "user": forms.Select(attrs={
                "class": "form-control"
            }),
        }
