from django import forms

from .models import BackupJob


class BackupJobForm(forms.ModelForm):
    class Meta:
        model = BackupJob
        fields = [
            "name",
            "description",
            "backup_type",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }
