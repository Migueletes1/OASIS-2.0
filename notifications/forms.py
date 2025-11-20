from django import forms

from .models import Notification


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ["recipient", "sender", "message", "type", "is_read"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 3}),
        }
