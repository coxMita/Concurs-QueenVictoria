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
