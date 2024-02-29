"""
Model for the companies' app
"""

from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    """
    Model used to represent a company
    """

    # Each company is associated to a User object
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)

    name = models.CharField(max_length=255, null=False)
    type = models.CharField(max_length=255, null=False)
    vat_number = models.CharField(max_length=255, null=False)
    pec = models.CharField(max_length=255, null=False)
    unique_company_code = models.CharField(max_length=255, null=False)

    class Meta:
        verbose_name = "Azienda"
        verbose_name_plural = "Aziende"
