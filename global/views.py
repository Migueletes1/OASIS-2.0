from django.shortcuts import render


def landing_page(request):
    return render(request, "landing.html")


def error_404(request, exception, template_name="error_404.html"):
    return render(request, template_name, status=404)


def error_500(request, template_name="error_500.html"):
    return render(request, template_name, status=500)


def search_results(request):
    query = request.GET.get("q", "").strip()
    context = {
        "query": query,
        "results": [],
    }
    return render(request, "search_results.html", context)
def landing_page(request):
    return render(request, "landing.html", {
        "delay": "1s"
    })

