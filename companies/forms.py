from django import forms
from .models import Company


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = [
            "name",
            "nit",
            "email",
            "phone",
            "address",
            "sector",
            "website",
            "description",
            "logo",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "nit": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "sector": forms.Select(attrs={"class": "form-control"}),
            "website": forms.URLInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "logo": forms.FileInput(attrs={"class": "form-control"}),
        }

    # --------------------------------------------------------
    # VALIDACIONES PERSONALIZADAS
    # --------------------------------------------------------

    def clean_nit(self):
        nit = self.cleaned_data.get("nit")

        if not nit.isdigit():
            raise forms.ValidationError("El NIT solo puede contener números.")

        if len(nit) < 8:
            raise forms.ValidationError("El NIT debe tener al menos 8 dígitos.")

        return nit

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if Company.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya existe una empresa registrada con este correo.")

        return email
