from django import forms
from .models import Assignment
from companies.models import Company
from projects.models import Project
from instructors.models import Instructor
from django.contrib.auth import get_user_model

User = get_user_model()


class AssignmentForm(forms.ModelForm):
    """
    Formulario para crear nuevas asignaciones.
    """

    class Meta:
        model = Assignment
        fields = [
            "project",
            "company",
            "instructor",
            "apprentices",
            "description",
            "status",
        ]

        widgets = {
            "project": forms.Select(attrs={"class": "form-control"}),
            "company": forms.Select(attrs={"class": "form-control"}),
            "instructor": forms.Select(attrs={"class": "form-control"}),
            "apprentices": forms.SelectMultiple(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }


class AssignmentUpdateForm(forms.ModelForm):
    """
    Formulario para editar asignaciones existentes.
    """

    class Meta:
        model = Assignment
        fields = [
            "project",
            "company",
            "instructor",
            "apprentices",
            "description",
            "status",
        ]

        widgets = {
            "project": forms.Select(attrs={"class": "form-control"}),
            "company": forms.Select(attrs={"class": "form-control"}),
            "instructor": forms.Select(attrs={"class": "form-control"}),
            "apprentices": forms.SelectMultiple(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }
