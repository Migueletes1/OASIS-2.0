from django.urls import path
from . import views

app_name = "companies"

urlpatterns = [
    # ----------------------------------------------------------
    # EMPRESAS — CRUD PRINCIPAL
    # ----------------------------------------------------------
    path("", views.CompanyListView.as_view(), name="company_list"),
    path("create/", views.CompanyCreateView.as_view(), name="company_create"),
    path("<int:pk>/", views.CompanyDetailView.as_view(), name="company_detail"),
    path("<int:pk>/edit/", views.CompanyUpdateView.as_view(), name="company_edit"),
    path("<int:pk>/delete/", views.CompanyDeleteView.as_view(), name="company_delete"),

    # ----------------------------------------------------------
    # APROBACIÓN / RECHAZO DE EMPRESAS (USADO POR ADMIN)
    # ----------------------------------------------------------
    path("<int:pk>/approve/", views.approve_company, name="company_approve"),
    path("<int:pk>/reject/", views.reject_company, name="company_reject"),

    # ----------------------------------------------------------
    # DASHBOARD / MÉTRICAS DE EMPRESA
    # ----------------------------------------------------------
    path("<int:pk>/dashboard/", views.CompanyDashboardView.as_view(), name="company_dashboard"),

    # ----------------------------------------------------------
    # PROYECTOS DE UNA EMPRESA
    # ----------------------------------------------------------
    path("<int:pk>/projects/", views.CompanyProjectsListView.as_view(), name="company_projects"),
    path("<int:pk>/projects/create/", views.CompanyProjectCreateView.as_view(), name="company_project_create"),

    # ----------------------------------------------------------
    # PERFIL PÚBLICO ( VISIBLE PARA APRENDICES )
    # ----------------------------------------------------------
    path("public/<int:pk>/", views.PublicCompanyProfileView.as_view(), name="company_public_profile"),

    # ----------------------------------------------------------
    # BÚSQUEDA Y FILTROS
    # ----------------------------------------------------------
    path("search/", views.CompanySearchView.as_view(), name="company_search"),
]
