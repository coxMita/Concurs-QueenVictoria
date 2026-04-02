from django import forms
from django.contrib import admin

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


# ─── Shared helpers ───────────────────────────────────────────────────────────


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if not data:
            return []
        if isinstance(data, (list, tuple)):
            return [single_file_clean(item, initial) for item in data]
        return [single_file_clean(data, initial)]


# ─── Archive ──────────────────────────────────────────────────────────────────


class ArchiveDocumentInline(admin.TabularInline):
    model = ArchiveDocument
    extra = 1
    fields = ("title", "file", "sort_order", "uploaded_at")
    readonly_fields = ("uploaded_at",)


class ArchiveFolderAdminForm(forms.ModelForm):
    bulk_upload_files = MultipleFileField(
        required=False,
        label="Incarcare batch PDF-uri",
        help_text="Poti selecta mai multe fisiere PDF deodata pentru acest folder.",
    )

    class Meta:
        model = ArchiveFolder
        fields = "__all__"


@admin.register(ArchiveFolder)
class ArchiveFolderAdmin(admin.ModelAdmin):
    form = ArchiveFolderAdminForm
    list_display = ("name", "sort_order", "created_at", "updated_at")
    list_editable = ("sort_order",)
    search_fields = ("name",)
    inlines = [ArchiveDocumentInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        uploaded_files = form.cleaned_data.get("bulk_upload_files", [])
        for uploaded_file in uploaded_files:
            ArchiveDocument.objects.create(
                folder=form.instance,
                file=uploaded_file,
                title=uploaded_file.name.rsplit(".", 1)[0],
            )


@admin.register(ArchiveDocument)
class ArchiveDocumentAdmin(admin.ModelAdmin):
    list_display = ("display_title", "folder", "sort_order", "uploaded_at")
    list_filter = ("folder",)
    list_editable = ("sort_order",)
    search_fields = ("title", "file")


# ─── Rezultate config ─────────────────────────────────────────────────────────


@admin.register(JudetConfig)
class JudetConfigAdmin(admin.ModelAdmin):
    list_display = ("name", "sort_order")
    list_editable = ("sort_order",)
    search_fields = ("name",)


@admin.register(EtapaConfig)
class EtapaConfigAdmin(admin.ModelAdmin):
    list_display = ("name", "sort_order")
    list_editable = ("sort_order",)
    search_fields = ("name",)


# ─── Rezultate ────────────────────────────────────────────────────────────────


class RezultateDocumentInline(admin.TabularInline):
    model = RezultateDocument
    extra = 1
    fields = ("title", "file", "sort_order", "uploaded_at")
    readonly_fields = ("uploaded_at",)


class RezultateEtapaAdminForm(forms.ModelForm):
    bulk_upload_files = MultipleFileField(
        required=False,
        label="Incarcare batch PDF-uri",
        help_text="Selecteaza mai multe PDF-uri deodata pentru aceasta etapa.",
    )

    class Meta:
        model = RezultateEtapa
        fields = "__all__"


class RezultateEtapaInline(admin.TabularInline):
    model = RezultateEtapa
    extra = 0
    fields = ("name", "sort_order")
    show_change_link = True


class RezultateJudetInline(admin.TabularInline):
    model = RezultateJudet
    extra = 0
    fields = ("name", "sort_order")
    show_change_link = True


@admin.register(RezultateYear)
class RezultateYearAdmin(admin.ModelAdmin):
    list_display = ("name", "sort_order", "created_at")
    list_editable = ("sort_order",)
    search_fields = ("name",)
    inlines = [RezultateJudetInline]
    actions = ["populate_from_config"]

    def _populate_year(self, year):
        judete_cfg = list(JudetConfig.objects.all())
        etape_cfg = list(EtapaConfig.objects.all())
        for j_cfg in judete_cfg:
            judet, _ = RezultateJudet.objects.get_or_create(
                year=year,
                name=j_cfg.name,
                defaults={"sort_order": j_cfg.sort_order},
            )
            for e_cfg in etape_cfg:
                RezultateEtapa.objects.get_or_create(
                    judet=judet,
                    name=e_cfg.name,
                    defaults={"sort_order": e_cfg.sort_order},
                )

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)
        if is_new:
            self._populate_year(obj)

    @admin.action(description="Regenereaza subfoldere din configurare (judete + etape)")
    def populate_from_config(self, request, queryset):
        for year in queryset:
            self._populate_year(year)
        self.message_user(request, "Subfoldere generate cu succes.")


@admin.register(RezultateJudet)
class RezultateJudetAdmin(admin.ModelAdmin):
    list_display = ("name", "year", "sort_order")
    list_filter = ("year",)
    list_editable = ("sort_order",)
    search_fields = ("name",)
    inlines = [RezultateEtapaInline]


@admin.register(RezultateEtapa)
class RezultateEtapaAdmin(admin.ModelAdmin):
    form = RezultateEtapaAdminForm
    list_display = ("name", "judet", "sort_order")
    list_filter = ("judet__year", "judet")
    list_editable = ("sort_order",)
    search_fields = ("name",)
    inlines = [RezultateDocumentInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        uploaded_files = form.cleaned_data.get("bulk_upload_files", [])
        for uploaded_file in uploaded_files:
            RezultateDocument.objects.create(
                etapa=form.instance,
                file=uploaded_file,
                title=uploaded_file.name.rsplit(".", 1)[0],
            )


@admin.register(RezultateDocument)
class RezultateDocumentAdmin(admin.ModelAdmin):
    list_display = ("display_title", "etapa", "sort_order", "uploaded_at")
    list_filter = ("etapa__judet__year", "etapa__judet", "etapa")
    list_editable = ("sort_order",)
    search_fields = ("title", "file")
