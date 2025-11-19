from django.urls import path
from . import views

app_name = "assignments"

urlpatterns = [
    path('', views.assignment_list, name='list'),
    path('create/', views.assignment_create, name='create'),
    path('<int:pk>/detail/', views.assignment_detail, name='detail'),
    path('<int:pk>/edit/', views.assignment_edit, name='edit'),
    path('<int:pk>/delete/', views.assignment_delete, name='delete'),
]
