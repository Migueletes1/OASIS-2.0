from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, render

from .models import AuditLog


@login_required
def audit_list(request):
    logs = AuditLog.objects.select_related("user").order_by("-created_at")
    module = request.GET.get("module")
    action = request.GET.get("action")

    if module:
        logs = logs.filter(module__icontains=module)
    if action:
        logs = logs.filter(action=action)

    modules_summary = AuditLog.objects.values("module").annotate(count=Count("id"))

    return render(
        request,
        "audit_list.html",
        {
            "logs": logs,
            "modules_summary": modules_summary,
            "filter_module": module,
            "filter_action": action,
        },
    )


@login_required
def audit_detail(request, pk):
    log = get_object_or_404(AuditLog, pk=pk)
    return render(request, "audit_detail.html", {"log": log})


@login_required
def audit_dashboard(request):
    stats = {
        "by_action": AuditLog.objects.values("action").annotate(count=Count("id")),
        "by_module": AuditLog.objects.values("module").annotate(count=Count("id")),
        "total": AuditLog.objects.count(),
    }
    recent = AuditLog.objects.select_related("user").order_by("-created_at")[:10]

    return render(request, "audit_dashboard.html", {"stats": stats, "recent": recent})
