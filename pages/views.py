from django.shortcuts import render

from .models import ArchiveFolder


def home(request):
    return render(request, "pages/home.html")


def informatii(request):
    return render(request, "pages/informatii.html")


def calendar_page(request):
    return render(request, "pages/calendar.html", {"page_title": "Calendar"})


def parteneri(request):
    return render(request, "pages/parteneri.html", {"page_title": "Parteneri"})


def surse(request):
    return render(request, "pages/blank_page.html", {"page_title": "Surse"})


def subiecte(request):
    return render(request, "pages/subiecte.html")


def rezultate(request):
    return render(request, "pages/blank_page.html", {"page_title": "Rezultate"})


def arhiva(request):
    folders = ArchiveFolder.objects.prefetch_related("documents").all()
    return render(request, "pages/arhiva.html", {"folders": folders})


def tematica(request):
    return render(request, "pages/tematica.html")


def regulament(request):
    return render(request, "pages/regulament.html")


def galerie(request):
    return render(request, "pages/galerie.html")
