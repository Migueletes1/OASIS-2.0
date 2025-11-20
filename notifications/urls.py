from django.urls import path

from . import views

app_name = "notifications"

urlpatterns = [
    path("", views.notification_list, name="notification_list"),
    path("create/", views.notification_create, name="notification_create"),
    path("<int:pk>/", views.notification_detail, name="notification_detail"),
    path("<int:pk>/mark-read/", views.notification_mark_read, name="notification_mark_read"),
    path("center/", views.notification_center, name="notification_center"),
]
