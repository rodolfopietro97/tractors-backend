from django.db import models


class BrandOnlineCredential(models.Model):
    """
    Represent a credential for online brand authentication
    """

    username = models.CharField(
        max_length=256, blank=False, verbose_name="Username del brand online"
    )
    password = models.CharField(
        max_length=256, blank=False, verbose_name="Password del brand online"
    )
    brand = models.ForeignKey(
        "Brand", on_delete=models.CASCADE, verbose_name="Brand della credenziale"
    )

    class Meta:
        verbose_name = "Credenziale del Brand"
        verbose_name_plural = "Credenziali dei Brand"

    def __str__(self):
        return f"{self.brand}: {self.username} - {self.password}"
