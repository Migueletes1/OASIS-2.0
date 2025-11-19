from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Assignment
from .forms import AssignmentForm


# -------------------------
# LISTAR ASIGNACIONES
# -------------------------
def assignment_list(request):
    assignments = Assignment.objects.all().order_by('-created_at')
    return render(request, "assignments/assignment_list.html", {"assignments": assignments})


# -------------------------
# DETALLE DE ASIGNACIÓN
# -------------------------
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    return render(request, "assignments/assignment_detail.html", {"assignment": assignment})


# -------------------------
# CREAR ASIGNACIÓN
# -------------------------
def assignment_create(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Asignación creada correctamente.")
            return redirect("assignments:list")
    else:
        form = AssignmentForm()

    return render(request, "assignments/assignment_form.html", {"form": form, "title": "Crear asignación"})


# -------------------------
# EDITAR ASIGNACIÓN
# -------------------------
def assignment_edit(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)

    if request.method == "POST":
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, "Asignación actualizada correctamente.")
            return redirect("assignments:detail", pk=pk)
    else:
        form = AssignmentForm(instance=assignment)

    return render(
        request,
        "assignments/assignment_form.html",
        {"form": form, "title": "Editar asignación"}
    )


# -------------------------
# ELIMINAR ASIGNACIÓN
# -------------------------
def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)

    if request.method == "POST":
        assignment.delete()
        messages.success(request, "Asignación eliminada correctamente.")
        return redirect("assignments:list")

    return render(
        request,
        "assignments/assignment_confirm_delete.html",
        {"assignment": assignment}
    )
