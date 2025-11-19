from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import (
    ListView, DetailView, CreateView,
    UpdateView, DeleteView, TemplateView
)

from .models import Company
from .forms import CompanyForm
from projects.models import Project


# --------------------------------------------------------------
# HELPERS
# --------------------------------------------------------------

def is_admin(user):
    return user.is_staff or user.is_superuser


admin_required = user_passes_test(is_admin)


# --------------------------------------------------------------
# LISTA DE EMPRESAS
# --------------------------------------------------------------

class CompanyListView(ListView):
    model = Company
    template_name = "companies/company_list.html"
    context_object_name = "companies"
    paginate_by = 10


# --------------------------------------------------------------
# DETALLE DE EMPRESA
# --------------------------------------------------------------

class CompanyDetailView(DetailView):
    model = Company
    template_name = "companies/company_detail.html"
    context_object_name = "company"


# --------------------------------------------------------------
# CREAR EMPRESA
# --------------------------------------------------------------

class CompanyCreateView(CreateView):
    model = Company
    form_class = CompanyForm
    template_name = "companies/company_form.html"
    success_url = reverse_lazy("companies:company_list")

    def form_valid(self, form):
        messages.success(self.request, "Empresa registrada correctamente.")
        return super().form_valid(form)


# --------------------------------------------------------------
# EDITAR EMPRESA
# --------------------------------------------------------------

class CompanyUpdateView(UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = "companies/company_form.html"
    success_url = reverse_lazy("companies:company_list")

    def form_valid(self, form):
        messages.success(self.request, "La información de la empresa ha sido actualizada.")
        return super().form_valid(form)


# --------------------------------------------------------------
# ELIMINAR EMPRESA
# --------------------------------------------------------------

class CompanyDeleteView(DeleteView):
    model = Company
    template_name = "companies/company_confirm_delete.html"
    success_url = reverse_lazy("companies:company_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Empresa eliminada correctamente.")
        return super().delete(request, *args, **kwargs)


# --------------------------------------------------------------
# APROBAR EMPRESA
# --------------------------------------------------------------

@login_required
@admin_required
def approve_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    company.is_approved = True
    company.save()

    messages.success(request, "Empresa aprobada correctamente.")
    return redirect("companies:company_detail", pk=pk)


# --------------------------------------------------------------
# RECHAZAR EMPRESA
# --------------------------------------------------------------

@login_required
@admin_required
def reject_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    company.is_approved = False
    company.save()

    messages.error(request, "La empresa ha sido rechazada.")
    return redirect("companies:company_detail", pk=pk)


# --------------------------------------------------------------
# DASHBOARD DE EMPRESA
# --------------------------------------------------------------

class CompanyDashboardView(TemplateView):
    template_name = "companies/company_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = get_object_or_404(Company, pk=self.kwargs["pk"])

        context["company"] = company
        context["projects_total"] = Project.objects.filter(company=company).count()
        context["projects_active"] = Project.objects.filter(company=company, status="en_progreso").count()
        context["projects_completed"] = Project.objects.filter(company=company, status="finalizado").count()

        return context


# --------------------------------------------------------------
# PROYECTOS DE UNA EMPRESA
# --------------------------------------------------------------

class CompanyProjectsListView(ListView):
    model = Project
    template_name = "companies/company_projects.html"
    context_object_name = "projects"

    def get_queryset(self):
        company = get_object_or_404(Company, pk=self.kwargs["pk"])
        return Project.objects.filter(company=company).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = get_object_or_404(Company, pk=self.kwargs["pk"])
        return context


# --------------------------------------------------------------
# CREAR PROYECTO DESDE UNA EMPRESA
# --------------------------------------------------------------

class CompanyProjectCreateView(CreateView):
    model = Project
    fields = [
        "title", "description", "knowledge_area",
        "budget", "max_apprentices", "start_date", "end_date"
    ]
    template_name = "companies/company_project_form.html"

    def form_valid(self, form):
        company = get_object_or_404(Company, pk=self.kwargs["pk"])
        form.instance.company = company
        messages.success(self.request, "Proyecto creado exitosamente.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("companies:company_projects", kwargs={"pk": self.kwargs["pk"]})


# --------------------------------------------------------------
# PERFIL PÚBLICO DE EMPRESA (visible para aprendices)
# --------------------------------------------------------------

class PublicCompanyProfileView(DetailView):
    model = Company
    template_name = "companies/company_public_profile.html"
    context_object_name = "company"


# --------------------------------------------------------------
# BÚSQUEDA / FILTROS
# --------------------------------------------------------------

class CompanySearchView(ListView):
    model = Company
    template_name = "companies/company_search.html"
    context_object_name = "companies"

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        return Company.objects.filter(name__icontains=query)
