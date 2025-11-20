from django.urls import path

from . import views

app_name = "attachments"

urlpatterns = [
    path("", views.attachment_list, name="attachment_list"),
    path("upload/", views.attachment_upload, name="attachment_upload"),
    path("<int:pk>/", views.attachment_detail, name="attachment_detail"),
]
