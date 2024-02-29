"""
Model for the customer's app
"""

from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    """
    Model used to represent a customer
    """

    # Each customer is associated to a User object
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)

    name = models.CharField(max_length=255, null=False, default="")
    surname = models.CharField(max_length=255, null=False, default="")
    fiscal_code = models.CharField(max_length=16, null=False, default="")

    phone_number = models.CharField(max_length=10, null=False, default="")

    # Address fields
    nation = models.CharField(max_length=255, null=False, default="")
    region = models.CharField(max_length=255, null=False, default="")
    council = models.CharField(max_length=255, null=False, default="")
    city = models.CharField(max_length=255, null=False, default="")
    address = models.CharField(max_length=255, null=False, default="")

    # Valid since ... @TODO

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clienti"
