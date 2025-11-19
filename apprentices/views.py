from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Apprentice
from .forms import ApprenticeForm


# LISTAR APRENDICES
def apprentice_list(request):
    apprentices = Apprentice.objects.all()
    return render(request, "apprentices/list.html", {"apprentices": apprentices})


# CREAR APRENDIZ
def apprentice_create(request):
    if request.method == "POST":
        form = ApprenticeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Aprendiz registrado correctamente.")
            return redirect("apprentices:list")
    else:
        form = ApprenticeForm()

    return render(request, "apprentices/create.html", {"form": form})


# DETALLE DEL APRENDIZ
def apprentice_detail(request, pk):
    apprentice = get_object_or_404(Apprentice, pk=pk)
    return render(request, "apprentices/detail.html", {"apprentice": apprentice})


# EDITAR APRENDIZ
def apprentice_edit(request, pk):
    apprentice = get_object_or_404(Apprentice, pk=pk)

    if request.method == "POST":
        form = ApprenticeForm(request.POST, instance=apprentice)
        if form.is_valid():
            form.save()
            messages.success(request, "Aprendiz actualizado correctamente.")
            return redirect("apprentices:list")
    else:
        form = ApprenticeForm(instance=apprentice)

    return render(request, "apprentices/edit.html", {"form": form, "apprentice": apprentice})


# ELIMINAR APRENDIZ
def apprentice_delete(request, pk):
    apprentice = get_object_or_404(Apprentice, pk=pk)

    if request.method == "POST":
        apprentice.delete()
        messages.success(request, "Aprendiz eliminado correctamente.")
        return redirect("apprentices:list")

    return render(request, "apprentices/delete.html", {"apprentice": apprentice})

