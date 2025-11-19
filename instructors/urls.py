from django.urls import path
from . import views

app_name = "instructors"

urlpatterns = [
    # LISTA DE INSTRUCTORES
    path("", views.instructor_list, name="list"),

    # CREACIÓN
    path("create/", views.instructor_create, name="create"),

    # DETALLE
    path("<int:pk>/detail/", views.instructor_detail, name="detail"),

    # EDITAR
    path("<int:pk>/edit/", views.instructor_edit, name="edit"),

    # ELIMINAR
    path("<int:pk>/delete/", views.instructor_delete, name="delete"),

    # DASHBOARD DEL INSTRUCTOR
    path("<int:pk>/dashboard/", views.instructor_dashboard, name="dashboard"),
]
