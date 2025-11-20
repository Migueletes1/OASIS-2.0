from django import forms

from .models import SystemSetting


class SystemSettingForm(forms.ModelForm):
    class Meta:
        model = SystemSetting
        fields = ["key", "value", "description", "is_active"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
        }
