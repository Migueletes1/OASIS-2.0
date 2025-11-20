from django import forms

from .models import ProjectAttachment


class ProjectAttachmentForm(forms.ModelForm):
    class Meta:
        model = ProjectAttachment
        fields = [
            "project",
            "uploaded_by",
            "file",
            "title",
            "description",
            "attachment_type",
            "is_public",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }
