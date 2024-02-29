"""
Model for BrandFile
"""

import os

from django.db import models


class BrandFile(models.Model):
    """
    Represent a Brand file
    """

    file = models.TextField(
        blank=False, null=False, verbose_name="File del Brand"
    )
    brand = models.ForeignKey(
        "Brand", on_delete=models.CASCADE, verbose_name="Brand del File"
    )
    description = models.TextField(
        blank=True, null=False, verbose_name="Descrizione del File"
    )

    class Meta:
        verbose_name = "File del Brand"
        verbose_name_plural = "Files dei Brand"

    def __str__(self):
        return os.path.basename(self.file.__str__())
