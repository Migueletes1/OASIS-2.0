from django import forms
from django.contrib.auth import get_user_model

from .models import ProgressTracking


class ProgressTrackingForm(forms.ModelForm):
    """Formulario principal para crear y actualizar avances."""

    class Meta:
        model = ProgressTracking
        fields = [
            "project",
            "apprentice",
            "instructor_reviewer",
            "title",
            "description",
            "progress_percentage",
            "status",
            "evidence_file",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "progress_percentage": forms.NumberInput(attrs={"min": 0, "max": 100}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_model = get_user_model()
        self.fields["apprentice"].queryset = user_model.objects.filter(rol="aprendiz")
        self.fields["instructor_reviewer"].queryset = user_model.objects.filter(rol="instructor")

    def clean_progress_percentage(self):
        value = self.cleaned_data.get("progress_percentage", 0)
        if not 0 <= value <= 100:
            raise forms.ValidationError("El porcentaje debe estar entre 0 y 100.")
        return value
