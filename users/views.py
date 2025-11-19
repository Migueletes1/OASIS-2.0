# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView, DetailView, UpdateView, ListView, TemplateView
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .forms import (
    UserLoginForm, UserRegisterForm, UserEditForm
)


# ----------------------------------------------------------
# LOGIN
# ----------------------------------------------------------
class UserLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        messages.success(self.request, "Inicio de sesión exitoso")
        return reverse_lazy("users:profile")


# ----------------------------------------------------------
# LOGOUT
# ----------------------------------------------------------
def user_logout(request):
    logout(request)
    messages.info(request, "Sesión cerrada correctamente")
    return redirect("users:login")


# ----------------------------------------------------------
# REGISTRO MULTIRROL
# ----------------------------------------------------------
class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Activación por correo
        user.save()
        messages.success(self.request, "Registro exitoso. Revisa tu correo para activar tu cuenta.")
        return super().form_valid(form)


# ----------------------------------------------------------
# ACTIVACIÓN DE CUENTA
# (simulación — puedes conectar con un token real)
# ----------------------------------------------------------
def activate_account(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, "Cuenta activada correctamente.")
    return redirect("users:login")


# ----------------------------------------------------------
# PERFIL DEL USUARIO
# ----------------------------------------------------------
class UserProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "users/profile.html"

    def get_object(self):
        return self.request.user


# ----------------------------------------------------------
# EDITAR PERFIL
# ----------------------------------------------------------
class UserEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserEditForm
    template_name = "users/edit_profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Perfil actualizado correctamente.")
        return super().form_valid(form)


# ----------------------------------------------------------
# LISTADO DE USUARIOS (solo administrador)
# ----------------------------------------------------------
class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "users/user_list.html"
    context_object_name = "users"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, "No tienes permisos para ver esta sección.")
            return redirect("users:profile")
        return super().dispatch(request, *args, **kwargs)


# ----------------------------------------------------------
# DETALLE DE USUARIO (solo admin)
# ----------------------------------------------------------
class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "users/user_detail.html"
    context_object_name = "user_obj"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, "No tienes permisos para ver esta sección.")
            return redirect("users:profile")
        return super().dispatch(request, *args, **kwargs)


# ----------------------------------------------------------
# PASSWORD RESET
# ----------------------------------------------------------
class ResetPasswordView(PasswordResetView):
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")


class ResetPasswordConfirmView(PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")


# ----------------------------------------------------------
# PANEL DE USUARIO (Dashboard simple)
# ----------------------------------------------------------
class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "users/dashboard.html"
