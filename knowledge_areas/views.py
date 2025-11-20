from collections import defaultdict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import KnowledgeAreaForm
from .models import KnowledgeArea


@login_required
def knowledgearea_list(request):
    """Listado y filtro básico de áreas de conocimiento."""

    query = request.GET.get("q", "").strip()
    show_inactive = request.GET.get("show_inactive") == "1"

    areas = KnowledgeArea.objects.all()
    if query:
        areas = areas.filter(name__icontains=query)
    if not show_inactive:
        areas = areas.filter(is_active=True)

    context = {
        "areas": areas.order_by("name"),
        "query": query,
        "show_inactive": show_inactive,
        "stats": {
            "total": KnowledgeArea.objects.count(),
            "active": KnowledgeArea.objects.filter(is_active=True).count(),
            "inactive": KnowledgeArea.objects.filter(is_active=False).count(),
        },
    }
    return render(request, "knowledgearea_list.html", context)


@login_required
def knowledgearea_detail(request, pk):
    area = get_object_or_404(KnowledgeArea, pk=pk)
    return render(request, "knowledgearea_detail.html", {"area": area})


@login_required
def knowledgearea_create(request):
    if request.method == "POST":
        form = KnowledgeAreaForm(request.POST)
        if form.is_valid():
            area = form.save()
            messages.success(request, "Área creada correctamente.")
            return redirect("knowledge:detail", pk=area.pk)
    else:
        form = KnowledgeAreaForm()

    return render(request, "knowledgearea_edit.html", {"form": form, "is_create": True})


@login_required
def knowledgearea_edit(request, pk):
    area = get_object_or_404(KnowledgeArea, pk=pk)

    if request.method == "POST":
        form = KnowledgeAreaForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            messages.success(request, "Área actualizada correctamente.")
            return redirect("knowledge:detail", pk=pk)
    else:
        form = KnowledgeAreaForm(instance=area)

    return render(request, "knowledgearea_edit.html", {"form": form, "area": area})


@login_required
def knowledgearea_tree(request):
    """Representación agrupada (tipo árbol) por inicial."""

    grouped = defaultdict(list)
    for area in KnowledgeArea.objects.order_by("name"):
        grouped[area.name[0].upper()].append(area)

    context = {
        "grouped_areas": dict(grouped),
        "total": KnowledgeArea.objects.count(),
    }
    return render(request, "knowledgearea_tree.html", context)
