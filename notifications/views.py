from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import NotificationForm
from .models import Notification


@login_required
def notification_list(request):
    notifications = Notification.objects.filter(recipient=request.user).select_related("sender").order_by("-created_at")
    status_filter = request.GET.get("status")
    if status_filter == "unread":
        notifications = notifications.filter(is_read=False)
    elif status_filter == "read":
        notifications = notifications.filter(is_read=True)

    context = {
        "notifications": notifications,
        "status_filter": status_filter,
    }
    return render(request, "notification_list.html", context)


@login_required
def notification_detail(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    if not notification.is_read:
        notification.is_read = True
        notification.save(update_fields=["is_read"])
    return render(request, "notification_detail.html", {"notification": notification})


@login_required
def notification_create(request):
    if request.method == "POST":
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            if not notification.sender:
                notification.sender = request.user
            notification.save()
            messages.success(request, "Notificación enviada correctamente.")
            return redirect("notifications:notification_list")
    else:
        form = NotificationForm(initial={"sender": request.user})

    return render(request, "notification_center.html", {"form": form})


@login_required
def notification_mark_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.is_read = True
    notification.save(update_fields=["is_read"])
    messages.info(request, "Notificación marcada como leída.")
    return redirect(request.GET.get("next", "notifications:notification_list"))


@login_required
def notification_center(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by("-created_at")[:10]
    unread_count = Notification.objects.filter(recipient=request.user, is_read=False).count()

    form = NotificationForm(initial={"sender": request.user})

    context = {
        "notifications": notifications,
        "unread_count": unread_count,
        "form": form,
    }
    return render(request, "notification_center.html", context)
