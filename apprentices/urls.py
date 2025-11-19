from django.urls import path
from . import views

app_name = "apprentices"

urlpatterns = [
    # LISTA
    path("", views.apprentice_list, name="list"),

    # CREAR APRENDIZ
    path("create/", views.apprentice_create, name="create"),

    # DETALLE
    path("<int:pk>/detail/", views.apprentice_detail, name="detail"),

    # EDITAR
    path("<int:pk>/edit/", views.apprentice_edit, name="edit"),

    # ELIMINAR
    path("<int:pk>/delete/", views.apprentice_delete, name="delete"),
]
