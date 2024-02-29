"""
This command is used to remove all brands from the database.
After running this command, the database will be empty of all brands.
User and other data will not be affected.
"""

from django.core.management.base import BaseCommand

from brands.models.brand_files import BrandFile
from brands.models.brand_online import BrandOnlineCredential
from brands.models.brands import Brand


class Command(BaseCommand):
    help = "Remove all brands from the database"

    def handle(self, *args, **options):
        BrandFile.objects.all().delete()
        BrandOnlineCredential.objects.all().delete()
        Brand.objects.all().delete()
        self.stdout.write("All previous brands have been removed from the database.")
