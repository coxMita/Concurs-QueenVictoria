from functools import wraps

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import (
    ArchiveDocument,
    ArchiveFolder,
    EtapaConfig,
    JudetConfig,
    RezultateDocument,
    RezultateEtapa,
    RezultateJudet,
    RezultateYear,
)


def panel_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect("panel_login")
        return view_func(request, *args, **kwargs)
    return wrapper


# ─── Auth ─────────────────────────────────────────────────────────────────────

def panel_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("panel_dashboard")
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect("panel_dashboard")
        messages.error(request, "Credentiale invalide sau cont fara acces de staff.")
    return render(request, "panel/login.html")


@require_POST
def panel_logout_view(request):
    logout(request)
    return redirect("panel_login")


# ─── Dashboard ────────────────────────────────────────────────────────────────

@panel_required
def panel_dashboard(request):
    return render(request, "panel/dashboard.html", {
        "current_section": "dashboard",
        "years_count": RezultateYear.objects.count(),
        "rez_docs_count": RezultateDocument.objects.count(),
        "archive_folders_count": ArchiveFolder.objects.count(),
        "archive_docs_count": ArchiveDocument.objects.count(),
        "recent_years": RezultateYear.objects.prefetch_related("judete").all()[:5],
        "recent_folders": ArchiveFolder.objects.prefetch_related("documents").all()[:5],
    })


# ─── Rezultate ────────────────────────────────────────────────────────────────

@panel_required
def panel_rezultate(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if name:
            year, created = RezultateYear.objects.get_or_create(name=name)
            if created:
                for j_cfg in JudetConfig.objects.all():
                    judet = RezultateJudet.objects.create(
                        year=year, name=j_cfg.name, sort_order=j_cfg.sort_order
                    )
                    for e_cfg in EtapaConfig.objects.all():
                        RezultateEtapa.objects.create(
                            judet=judet, name=e_cfg.name, sort_order=e_cfg.sort_order
                        )
                messages.success(request, f"Anul {name} a fost creat cu subfoldere din configurare.")
            else:
                messages.warning(request, f"Anul {name} exista deja.")
        return redirect("panel_rezultate")
    years = RezultateYear.objects.prefetch_related("judete__etape__documents").all()
    return render(request, "panel/rezultate_years.html", {
        "current_section": "rezultate",
        "years": years,
    })


@panel_required
@require_POST
def panel_rezultate_year_delete(request, year_id):
    year = get_object_or_404(RezultateYear, pk=year_id)
    name = year.name
    year.delete()
    messages.success(request, f"Anul {name} a fost sters.")
    return redirect("panel_rezultate")


@panel_required
def panel_rezultate_year(request, year_id):
    year = get_object_or_404(RezultateYear, pk=year_id)
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if name:
            judet, created = RezultateJudet.objects.get_or_create(year=year, name=name)
            if created:
                for e_cfg in EtapaConfig.objects.all():
                    RezultateEtapa.objects.create(
                        judet=judet, name=e_cfg.name, sort_order=e_cfg.sort_order
                    )
                messages.success(request, f"Judetul {name} a fost adaugat cu etape din configurare.")
            else:
                messages.warning(request, f"Judetul {name} exista deja pentru {year.name}.")
        return redirect("panel_rezultate_year", year_id=year_id)
    judete = year.judete.prefetch_related("etape__documents").all()
    return render(request, "panel/rezultate_judete.html", {
        "current_section": "rezultate",
        "year": year,
        "judete": judete,
    })


@panel_required
@require_POST
def panel_rezultate_judet_delete(request, year_id, judet_id):
    judet = get_object_or_404(RezultateJudet, pk=judet_id, year_id=year_id)
    name = judet.name
    judet.delete()
    messages.success(request, f"Judetul {name} a fost sters.")
    return redirect("panel_rezultate_year", year_id=year_id)


@panel_required
def panel_rezultate_judet(request, year_id, judet_id):
    year = get_object_or_404(RezultateYear, pk=year_id)
    judet = get_object_or_404(RezultateJudet, pk=judet_id, year=year)
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if name:
            _, created = RezultateEtapa.objects.get_or_create(judet=judet, name=name)
            if created:
                messages.success(request, f"Etapa {name} a fost adaugata.")
            else:
                messages.warning(request, f"Etapa {name} exista deja.")
        return redirect("panel_rezultate_judet", year_id=year_id, judet_id=judet_id)
    etape = judet.etape.prefetch_related("documents").all()
    return render(request, "panel/rezultate_etape.html", {
        "current_section": "rezultate",
        "year": year,
        "judet": judet,
        "etape": etape,
    })


@panel_required
@require_POST
def panel_rezultate_etapa_delete(request, year_id, judet_id, etapa_id):
    etapa = get_object_or_404(RezultateEtapa, pk=etapa_id, judet_id=judet_id)
    name = etapa.name
    etapa.delete()
    messages.success(request, f"Etapa {name} a fost stearsa.")
    return redirect("panel_rezultate_judet", year_id=year_id, judet_id=judet_id)


@panel_required
def panel_rezultate_etapa(request, year_id, judet_id, etapa_id):
    year = get_object_or_404(RezultateYear, pk=year_id)
    judet = get_object_or_404(RezultateJudet, pk=judet_id, year=year)
    etapa = get_object_or_404(RezultateEtapa, pk=etapa_id, judet=judet)
    if request.method == "POST":
        files = request.FILES.getlist("files")
        count = 0
        for f in files:
            RezultateDocument.objects.create(
                etapa=etapa,
                file=f,
                title=f.name.rsplit(".", 1)[0],
            )
            count += 1
        if count:
            messages.success(request, f"{count} fisier(e) incarcate cu succes.")
        return redirect("panel_rezultate_etapa", year_id=year_id, judet_id=judet_id, etapa_id=etapa_id)
    docs = etapa.documents.all()
    return render(request, "panel/rezultate_docs.html", {
        "current_section": "rezultate",
        "year": year,
        "judet": judet,
        "etapa": etapa,
        "docs": docs,
    })


@panel_required
@require_POST
def panel_rezultate_doc_delete(request, year_id, judet_id, etapa_id, doc_id):
    doc = get_object_or_404(RezultateDocument, pk=doc_id, etapa_id=etapa_id)
    doc.file.delete(save=False)
    doc.delete()
    messages.success(request, "Documentul a fost sters.")
    return redirect("panel_rezultate_etapa", year_id=year_id, judet_id=judet_id, etapa_id=etapa_id)


# ─── Config ───────────────────────────────────────────────────────────────────

@panel_required
def panel_config(request):
    if request.method == "POST":
        action = request.POST.get("action", "")
        if action == "add_judet":
            name = request.POST.get("name", "").strip()
            if name:
                _, created = JudetConfig.objects.get_or_create(name=name)
                if created:
                    messages.success(request, f"Judetul '{name}' adaugat in configurare.")
                else:
                    messages.warning(request, f"Judetul '{name}' exista deja.")
        elif action == "del_judet":
            pk = request.POST.get("pk")
            JudetConfig.objects.filter(pk=pk).delete()
            messages.success(request, "Judetul a fost sters din configurare.")
        elif action == "add_etapa":
            name = request.POST.get("name", "").strip()
            if name:
                _, created = EtapaConfig.objects.get_or_create(name=name)
                if created:
                    messages.success(request, f"Etapa '{name}' adaugata in configurare.")
                else:
                    messages.warning(request, f"Etapa '{name}' exista deja.")
        elif action == "del_etapa":
            pk = request.POST.get("pk")
            EtapaConfig.objects.filter(pk=pk).delete()
            messages.success(request, "Etapa a fost stearsa din configurare.")
        return redirect("panel_config")
    return render(request, "panel/config.html", {
        "current_section": "config",
        "judete": JudetConfig.objects.all(),
        "etape": EtapaConfig.objects.all(),
    })


# ─── Arhiva ───────────────────────────────────────────────────────────────────

@panel_required
def panel_arhiva(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if name:
            _, created = ArchiveFolder.objects.get_or_create(name=name)
            if created:
                messages.success(request, f"Folderul '{name}' a fost creat.")
            else:
                messages.warning(request, f"Folderul '{name}' exista deja.")
        return redirect("panel_arhiva")
    folders = ArchiveFolder.objects.prefetch_related("documents").all()
    return render(request, "panel/arhiva.html", {
        "current_section": "arhiva",
        "folders": folders,
    })


@panel_required
@require_POST
def panel_arhiva_folder_delete(request, folder_id):
    folder = get_object_or_404(ArchiveFolder, pk=folder_id)
    name = folder.name
    folder.delete()
    messages.success(request, f"Folderul '{name}' a fost sters.")
    return redirect("panel_arhiva")


@panel_required
def panel_arhiva_folder(request, folder_id):
    folder = get_object_or_404(ArchiveFolder, pk=folder_id)
    if request.method == "POST":
        files = request.FILES.getlist("files")
        count = 0
        for f in files:
            ArchiveDocument.objects.create(
                folder=folder,
                file=f,
                title=f.name.rsplit(".", 1)[0],
            )
            count += 1
        if count:
            messages.success(request, f"{count} fisier(e) incarcate cu succes.")
        return redirect("panel_arhiva_folder", folder_id=folder_id)
    docs = folder.documents.all()
    return render(request, "panel/arhiva_folder.html", {
        "current_section": "arhiva",
        "folder": folder,
        "docs": docs,
    })


@panel_required
@require_POST
def panel_arhiva_doc_delete(request, folder_id, doc_id):
    doc = get_object_or_404(ArchiveDocument, pk=doc_id, folder_id=folder_id)
    doc.file.delete(save=False)
    doc.delete()
    messages.success(request, "Documentul a fost sters.")
    return redirect("panel_arhiva_folder", folder_id=folder_id)
