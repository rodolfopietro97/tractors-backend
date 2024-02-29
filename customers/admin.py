"""
Admin configuration for the customer's app.
"""

from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Admin configuration for the customer model.
    """

    pass
