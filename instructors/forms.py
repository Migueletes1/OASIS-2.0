from django import forms
from .models import Instructor


class InstructorForm(forms.ModelForm):
    """Formulario para crear un instructor"""

    class Meta:
        model = Instructor
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "specialty",
            "avatar",
            "is_active",
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre del instructor"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Apellidos del instructor"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "correo@ejemplo.com"
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Número de contacto"
            }),
            "specialty": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Área o especialidad"
            }),
            "avatar": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }


class InstructorEditForm(forms.ModelForm):
    """Formulario para editar un instructor"""

    class Meta:
        model = Instructor
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "specialty",
            "avatar",
            "is_active",
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control"
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "specialty": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "avatar": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }
