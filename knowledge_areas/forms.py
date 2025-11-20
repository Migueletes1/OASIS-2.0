from django import forms

from .models import KnowledgeArea


class KnowledgeAreaForm(forms.ModelForm):
    class Meta:
        model = KnowledgeArea
        fields = ["name", "description", "is_active"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }
