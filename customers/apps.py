"""
Main app configuration for the customer's app.
"""

from django.apps import AppConfig


class CustomersConfig(AppConfig):
    """
    Configuration for the customer's app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "customers"
