from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def help_index(request):
    sections = [
        {"title": "Preguntas frecuentes", "url": "help:faq"},
        {"title": "Guías paso a paso", "url": "help:guides"},
    ]
    return render(request, "help_index.html", {"sections": sections})


@login_required
def help_faq(request):
    faqs = [
        {
            "question": "¿Cómo registro un nuevo proyecto?",
            "answer": "Ingresa a Proyectos > Crear y completa el formulario.",
        },
        {
            "question": "¿Dónde consulto mis notificaciones?",
            "answer": "Ve al centro de notificaciones desde el ícono de campana.",
        },
    ]
    return render(request, "help_faq.html", {"faqs": faqs})


@login_required
def help_guides(request):
    guides = [
        {
            "title": "Asignar aprendices a un proyecto",
            "steps": [
                "Crea o edita un proyecto",
                "En la sección de asignaciones, agrega aprendices",
                "Guarda los cambios",
            ],
        },
        {
            "title": "Registrar un avance",
            "steps": [
                "Ingresa a Seguimiento",
                "Haz clic en \"Registrar avance\"",
                "Adjunta evidencia y envía para revisión",
            ],
        },
    ]
    return render(request, "help_guides.html", {"guides": guides})
