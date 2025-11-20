from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProjectAttachmentForm
from .models import ProjectAttachment


@login_required
def attachment_list(request):
    attachments = ProjectAttachment.objects.select_related("project", "uploaded_by")

    user_role = getattr(request.user, "rol", None)
    if user_role == "aprendiz":
        attachments = attachments.filter(
            Q(is_public=True) | Q(project__apprentices=request.user) | Q(uploaded_by=request.user)
        ).distinct()

    context = {
        "attachments": attachments.order_by("-uploaded_at"),
    }
    return render(request, "attachment_list.html", context)


@login_required
def attachment_detail(request, pk):
    attachment = get_object_or_404(ProjectAttachment, pk=pk)

    if getattr(request.user, "rol", None) == "aprendiz" and not (
        attachment.is_public
        or attachment.uploaded_by == request.user
        or request.user in attachment.project.apprentices.all()
    ):
        messages.error(request, "No tienes permisos para ver este archivo.")
        return redirect("attachments:attachment_list")

    return render(request, "attachment_detail.html", {"attachment": attachment})


@login_required
def attachment_upload(request):
    if request.method == "POST":
        form = ProjectAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            if not attachment.uploaded_by:
                attachment.uploaded_by = request.user
            attachment.save()
            messages.success(request, "Archivo cargado correctamente.")
            return redirect("attachments:attachment_detail", pk=attachment.pk)
    else:
        form = ProjectAttachmentForm(initial={"uploaded_by": request.user})

    return render(request, "attachment_upload.html", {"form": form})
