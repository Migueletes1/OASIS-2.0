# users/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser


# ----------------------------------------------------------
# LOGIN FORM
# ----------------------------------------------------------
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "ejemplo@correo.com"
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "********"
        })
    )


# ----------------------------------------------------------
# REGISTRO MULTIRROL
# ----------------------------------------------------------
class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "********"
        })
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "********"
        })
    )

    ROLE_CHOICES = [
        ("empresa", "Empresa"),
        ("instructor", "Instructor"),
        ("aprendiz", "Aprendiz"),
    ]

    role = forms.ChoiceField(
        label="Rol",
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = CustomUser
        fields = ("fullname", "email", "role")
        widgets = {
            "fullname": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre completo"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "ejemplo@correo.com"
            }),
        }

    # ------------ VALIDACIONES ------------
    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise ValidationError("Las contraseñas no coinciden.")
        return p2

    def clean_email(self):
        email = self.cleaned_data["email"]
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Este correo ya está registrado.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # rol se asigna desde el campo
        user.role = self.cleaned_data["role"]
        if commit:
            user.save()
        return user


# ----------------------------------------------------------
# EDITAR PERFIL
# ----------------------------------------------------------
class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("fullname", "email", "avatar")
        widgets = {
            "fullname": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre completo"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Correo electrónico"
            }),
            "avatar": forms.FileInput(attrs={
                "class": "form-control"
            }),
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        qs = CustomUser.objects.filter(email=email).exclude(id=self.instance.id)
        if qs.exists():
            raise ValidationError("Este correo ya está en uso por otro usuario.")
        return email
