from django import forms
from django.contrib import admin

from .models import ArchiveDocument, ArchiveFolder


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
