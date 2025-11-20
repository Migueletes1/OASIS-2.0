from django import forms

from .models import AuditLog


class AuditLogForm(forms.ModelForm):
    class Meta:
        model = AuditLog
        fields = ["module", "action", "description", "ip_address"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }
