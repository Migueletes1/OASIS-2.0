from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SystemSettingForm
from .models import SystemSetting


@login_required
def config_list(request):
    settings_qs = SystemSetting.objects.all().order_by("key")
    return render(request, "config_list.html", {"settings": settings_qs})


@login_required
def config_detail(request, pk):
    setting = get_object_or_404(SystemSetting, pk=pk)
    return render(request, "config_detail.html", {"setting": setting})


@login_required
def config_edit(request, pk):
    setting = get_object_or_404(SystemSetting, pk=pk)

    if request.method == "POST":
        form = SystemSettingForm(request.POST, instance=setting)
        if form.is_valid():
            form.save()
            messages.success(request, "Configuración actualizada correctamente.")
            return redirect("system:config_detail", pk=pk)
    else:
        form = SystemSettingForm(instance=setting)

    return render(request, "config_edit.html", {"form": form, "setting": setting})
