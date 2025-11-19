from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Project
from .forms import ProjectForm


# LISTA DE PROYECTOS
def project_list(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'projects/project_list.html', {'projects': projects})


# DETALLE DE UN PROYECTO
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project_detail.html', {'project': project})


# CREAR PROYECTO
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Proyecto creado exitosamente.")
            return redirect('projects:project_list')
    else:
        form = ProjectForm()

    return render(request, 'projects/project_form.html', {'form': form})


# EDITAR PROYECTO
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Proyecto actualizado correctamente.")
            return redirect('projects:project_detail', pk=pk)
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projects/project_form.html', {'form': form, 'project': project})


# ELIMINAR PROYECTO
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Proyecto eliminado correctamente.")
        return redirect('projects:project_list')

    return render(request, 'projects/project_confirm_delete.html', {'project': project})

