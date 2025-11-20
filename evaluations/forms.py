from django import forms
from django.contrib.auth import get_user_model

from .models import Evaluation


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = [
            "project",
            "apprentice",
            "evaluator",
            "score",
            "observations",
            "status",
            "report_file",
        ]
        widgets = {
            "observations": forms.Textarea(attrs={"rows": 4}),
            "score": forms.NumberInput(attrs={"min": 0, "max": 100}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_model = get_user_model()
        self.fields["apprentice"].queryset = user_model.objects.filter(rol="aprendiz")
        self.fields["evaluator"].queryset = user_model.objects.filter(rol__in=["instructor", "admin"])

    def clean_score(self):
        score = self.cleaned_data.get("score", 0)
        if not 0 <= score <= 100:
            raise forms.ValidationError("El puntaje debe estar entre 0 y 100.")
        return score
