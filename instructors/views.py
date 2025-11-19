from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Instructor
from .forms import InstructorForm


# ============================
#   LISTA DE INSTRUCTORES
# ============================
@login_required
def instructor_list(request):
    instructors = Instructor.objects.all().order_by("full_name")
    return render(request, "instructors/instructor_list.html", {"instructors": instructors})


# ============================
#     CREAR INSTRUCTOR
# ============================
@login_required
def instructor_create(request):
    if request.method == "POST":
        form = InstructorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Instructor creado correctamente.")
            return redirect("instructors:list")
    else:
        form = InstructorForm()

    return render(request, "instructors/instructor_create.html", {"form": form})


# ============================
#   DETALLE DEL INSTRUCTOR
# ============================
@login_required
def instructor_detail(request, pk):
    instructor = get_object_or_404(Instructor, pk=pk)
    return render(request, "instructors/instructor_detail.html", {"instructor": instructor})


# ============================
#    EDITAR INSTRUCTOR
# ============================
@login_required
def instructor_edit(request, pk):
    instructor = get_object_or_404(Instructor, pk=pk)

    if request.method == "POST":
        form = InstructorForm(request.POST, request.FILES, instance=instructor)
        if form.is_valid():
            form.save()
            messages.success(request, "Instructor actualizado correctamente.")
            return redirect("instructors:detail", pk=instructor.pk)
    else:
        form = InstructorForm(instance=instructor)

    return render(request, "instructors/instructor_edit.html", {"form": form, "instructor": instructor})


# ============================
#   ELIMINAR INSTRUCTOR
# ============================
@login_required
def instructor_delete(request, pk):
    instructor = get_object_or_404(Instructor, pk=pk)

    if request.method == "POST":
        instructor.delete()
        messages.success(request, "Instructor eliminado correctamente.")
        return redirect("instructors:list")

    return render(request, "instructors/instructor_delete.html", {"instructor": instructor})


# ============================
#   DASHBOARD DE INSTRUCTOR
# ============================
@login_required
def instructor_dashboard(request, pk):
    instructor = get_object_or_404(Instructor, pk=pk)

    # Si luego conectas assignments:
    # assignments = instructor.assignments_set.all()
    # proyectos_activos = assignments.filter(status="en_progreso")

    context = {
        "instructor": instructor,
        # "assignments": assignments,
        # "proyectos_activos": proyectos_activos,
    }

    return render(request, "instructors/instructor_dashboard.html", context)
