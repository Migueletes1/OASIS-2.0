from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'description',
            'objective',
            'company',
            'status',
            'start_date',
            'end_date',
            'apprentices',
        ]

        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'objective': forms.Textarea(attrs={'rows': 3}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'apprentices': forms.SelectMultiple(attrs={'size': 6}),
        }