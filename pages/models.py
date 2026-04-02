import os

from django.core.validators import FileExtensionValidator
from django.db import models


def archive_document_upload_path(instance, filename):
    folder_name = instance.folder.name.strip().replace(" ", "_")
    return f"archive/{folder_name}/{filename}"


class ArchiveFolder(models.Model):
    name = models.CharField(max_length=100, unique=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "-name"]
        verbose_name = "Folder arhiva"
        verbose_name_plural = "Foldere arhiva"

    def __str__(self):
        return self.name


class ArchiveDocument(models.Model):
    folder = models.ForeignKey(
        ArchiveFolder,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name="Folder",
    )
    title = models.CharField(max_length=200, blank=True)
    file = models.FileField(
        upload_to=archive_document_upload_path,
        validators=[FileExtensionValidator(["pdf"])],
        verbose_name="Fisier PDF",
    )
    sort_order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "title", "file"]
        verbose_name = "Document arhiva"
        verbose_name_plural = "Documente arhiva"

    def __str__(self):
        return self.display_title

    @property
    def display_title(self):
        if self.title:
            return self.title
        return os.path.basename(self.file.name)


# ─── Rezultate ────────────────────────────────────────────────────────────────


class JudetConfig(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Judet")
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "Judet (configurare)"
        verbose_name_plural = "Judete (configurare)"

    def __str__(self):
        return self.name


class EtapaConfig(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Etapa")
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "Etapa (configurare)"
        verbose_name_plural = "Etape (configurare)"

    def __str__(self):
        return self.name


class RezultateYear(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name="An")
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "-name"]
        verbose_name = "An rezultate"
        verbose_name_plural = "Ani rezultate"

    def __str__(self):
        return self.name


class RezultateJudet(models.Model):
    year = models.ForeignKey(
        RezultateYear,
        on_delete=models.CASCADE,
        related_name="judete",
        verbose_name="An",
    )
    name = models.CharField(max_length=100, verbose_name="Judet")
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        unique_together = ("year", "name")
        verbose_name = "Judet rezultate"
        verbose_name_plural = "Judete rezultate"

    def __str__(self):
        return f"{self.year.name} / {self.name}"


class RezultateEtapa(models.Model):
    judet = models.ForeignKey(
        RezultateJudet,
        on_delete=models.CASCADE,
        related_name="etape",
        verbose_name="Judet",
    )
    name = models.CharField(max_length=100, verbose_name="Etapa")
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        unique_together = ("judet", "name")
        verbose_name = "Etapa rezultate"
        verbose_name_plural = "Etape rezultate"

    def __str__(self):
        return f"{self.judet} / {self.name}"


def rezultate_document_upload_path(instance, filename):
    year_name = instance.etapa.judet.year.name.strip().replace(" ", "_")
    judet_name = instance.etapa.judet.name.strip().replace(" ", "_")
    etapa_name = instance.etapa.name.strip().replace(" ", "_")
    return f"rezultate/{year_name}/{judet_name}/{etapa_name}/{filename}"


class RezultateDocument(models.Model):
    etapa = models.ForeignKey(
        RezultateEtapa,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name="Etapa",
    )
    title = models.CharField(max_length=200, blank=True, verbose_name="Titlu")
    file = models.FileField(
        upload_to=rezultate_document_upload_path,
        validators=[FileExtensionValidator(["pdf"])],
        verbose_name="Fisier PDF",
    )
    sort_order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "title", "file"]
        verbose_name = "Document rezultate"
        verbose_name_plural = "Documente rezultate"

    def __str__(self):
        return self.display_title

    @property
    def display_title(self):
        if self.title:
            return self.title
        return os.path.basename(self.file.name)
