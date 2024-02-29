"""
Brands model
"""

from django.db import models


class Brand(models.Model):
    """
    Represent a Brand
    """

    name = models.CharField(
        primary_key=True,
        max_length=100,
        blank=False,
        null=False,
        verbose_name="Nome del Brand",
    )

    image = models.TextField(blank=False, null=False, verbose_name="Immagine del Brand")

    brand_online_url = models.URLField(
        max_length=500, blank=True, null=True, verbose_name="URL del Brand Online"
    )

    class Categories(models.TextChoices):
        """
        Possible categories of a Brand
        """

        TRACTORS = "Trattori", "Trattori"
        EQUIPMENT = "Attrezzature", "Attrezzature"
        BOTH = "Entrambi", "Entrambi"

    # Category of the Brand enum
    category = models.CharField(
        max_length=12,
        choices=Categories.choices,
        default=Categories.TRACTORS,
        verbose_name="Categoria del Brand",
    )

    class Types(models.TextChoices):
        """
        Possible categories of a Brand
        """

        ONLINE = "Online", "Online"
        PDF = "PDF", "PDF"
        BOTH = "Entrambi", "Entrambi"

    # Type of the Brand enum
    type = models.CharField(
        max_length=12,
        choices=Types.choices,
        default=Types.ONLINE,
        verbose_name="Typo del Brand",
    )

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return f"{self.name}"
