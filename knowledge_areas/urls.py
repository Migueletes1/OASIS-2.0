from django.urls import path

from . import views

app_name = "knowledge"

urlpatterns = [
    path("", views.knowledgearea_list, name="list"),
    path("create/", views.knowledgearea_create, name="create"),
    path("<int:pk>/", views.knowledgearea_detail, name="detail"),
    path("<int:pk>/edit/", views.knowledgearea_edit, name="edit"),
    path("tree/", views.knowledgearea_tree, name="tree"),
]
