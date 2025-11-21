"""
URL configuration for OASIS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from importlib import import_module

global_views = import_module("global.views")

urlpatterns = [
    path('admin/', admin.site.urls),

    # Apps principales
    path('', global_views.landing_page, name='landing'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls', namespace='users')),
    path('companies/', include('companies.urls', namespace='companies')),
    path('apprentices/', include('apprentices.urls', namespace='apprentices')),
    path('instructors/', include('instructors.urls', namespace='instructors')),
    path('projects/', include('projects.urls', namespace='projects')),
    path('assignments/', include('assignments.urls', namespace='assignments')),
    path('progress/', include('progress_tracking.urls', namespace='progress')),
    path('evaluations/', include('evaluations.urls', namespace='evaluations')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    path('attachments/', include('project_attachments.urls', namespace='attachments')),
    path('knowledge/', include('knowledge_areas.urls', namespace='knowledge')),
    path('reports/', include('reports.urls', namespace='reports')),
    path('system/', include('system_config.urls', namespace='system')),
    path('help/', include('help.urls', namespace='help')),
    path('backup/', include('backups.urls', namespace='backup')),
    path('audit/', include('audit_logs.urls', namespace='audit')),
    path('global/', include('global.urls', namespace='global')),   # Errores, páginas generales, landing page
]

# Archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
