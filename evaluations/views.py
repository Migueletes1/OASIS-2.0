from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EvaluationForm
from .models import Evaluation


@login_required
def evaluation_list(request):
    evaluations = Evaluation.objects.select_related("project", "apprentice", "evaluator")
    if getattr(request.user, "rol", None) == "aprendiz":
        evaluations = evaluations.filter(apprentice=request.user)
    elif getattr(request.user, "rol", None) == "instructor":
        evaluations = evaluations.filter(Q(evaluator=request.user) | Q(apprentice=request.user))

    return render(request, "evaluation_list.html", {"evaluations": evaluations})


@login_required
def evaluation_detail(request, pk):
    evaluation = get_object_or_404(Evaluation, pk=pk)
    if request.user not in {evaluation.apprentice, evaluation.evaluator} and not request.user.is_staff:
        messages.error(request, "No tienes permisos para ver esta evaluación.")
        return redirect("evaluations:evaluation_list")

    return render(request, "evaluation_detail.html", {"evaluation": evaluation})


@login_required
def evaluation_create(request):
    if request.method == "POST":
        form = EvaluationForm(request.POST, request.FILES)
        if form.is_valid():
            evaluation = form.save(commit=False)
            if getattr(request.user, "rol", None) == "instructor":
                evaluation.evaluator = request.user
            evaluation.save()
            messages.success(request, "Evaluación registrada correctamente.")
            return redirect("evaluations:evaluation_detail", pk=evaluation.pk)
    else:
        form = EvaluationForm(initial={"evaluator": request.user})

    return render(request, "evaluation_create.html", {"form": form})


@login_required
def evaluation_edit(request, pk):
    evaluation = get_object_or_404(Evaluation, pk=pk)
    if request.user not in {evaluation.evaluator} and not request.user.is_staff:
        messages.error(request, "No tienes permisos para editar esta evaluación.")
        return redirect("evaluations:evaluation_detail", pk=pk)

    if request.method == "POST":
        form = EvaluationForm(request.POST, request.FILES, instance=evaluation)
        if form.is_valid():
            form.save()
            messages.success(request, "Evaluación actualizada correctamente.")
            return redirect("evaluations:evaluation_detail", pk=pk)
    else:
        form = EvaluationForm(instance=evaluation)

    return render(request, "evaluation_edit.html", {"form": form, "evaluation": evaluation})


@login_required
def evaluation_dashboard(request):
    evaluations = Evaluation.objects.all()
    context = {
        "totals": {
            "total": evaluations.count(),
            "pending": evaluations.filter(status="pending").count(),
            "approved": evaluations.filter(status="approved").count(),
            "rejected": evaluations.filter(status="rejected").count(),
            "completed": evaluations.filter(status="completed").count(),
        },
        "average_scores": evaluations.values("project__title").annotate(
            avg_score=Avg("score"),
            evaluations=Count("id"),
        ),
    }
    return render(request, "evaluation_dashboard.html", context)


@login_required
def evaluation_report(request):
    reports = (
        Evaluation.objects.values("project__title", "status")
        .annotate(count=Count("id"), avg_score=Avg("score"))
        .order_by("project__title")
    )
    return render(request, "evaluation_report.html", {"reports": reports})
