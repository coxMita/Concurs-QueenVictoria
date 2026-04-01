from django.shortcuts import render


def home(request):
    return render(request, 'core/home.html')


def informatii(request):
    return render(request, 'core/informatii.html')


def calendar(request):
    return render(request, 'core/calendar.html')


def parteneri(request):
    return render(request, 'core/parteneri.html')


def surse(request):
    return render(request, 'core/surse.html')


def subiecte(request):
    return render(request, 'core/subiecte.html')


def rezultate(request):
    results = []
    return render(request, 'core/rezultate.html', {'results': results})


def arhiva(request):
    return render(request, 'core/arhiva.html')


def tematica(request):
    return render(request, 'core/tematica.html')


def regulament(request):
    return render(request, 'core/regulament.html')


def galerie(request):
    gallery_images = []
    return render(request, 'core/galerie.html', {'gallery_images': gallery_images})
