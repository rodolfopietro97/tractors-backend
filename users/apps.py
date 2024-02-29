"""
Main app configuration for the user's app.
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Configuration for the user's app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"