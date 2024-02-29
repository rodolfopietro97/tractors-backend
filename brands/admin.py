"""
Admin configuration for the brands' app.
"""

from django.contrib import admin

from .models.brand_files import BrandFile
from .models.brand_online import BrandOnlineCredential
from .models.brands import Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Brand model.
    """

    pass


@admin.register(BrandFile)
class BrandFileAdmin(admin.ModelAdmin):
    """
    Admin configuration for the BrandFile model.
    """

    pass


@admin.register(BrandOnlineCredential)
class BrandOnlineCredentialAdmin(admin.ModelAdmin):
    """
    Admin configuration for the BrandOnlineCredential model.
    """

    pass
