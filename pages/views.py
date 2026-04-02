from django.shortcuts import render


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
    return render(request, "pages/blank_page.html", {"page_title": "Arhiva"})


def tematica(request):
    return render(request, "pages/tematica.html")


def regulament(request):
    return render(request, "pages/regulament.html")


def galerie(request):
    return render(request, "pages/blank_page.html", {"page_title": "Galerie"})
