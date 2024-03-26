"""
This command is used to import all brands from cloud storage to the database.
After running this command, the database will have all brands.
NOTE: User and other data will not be affected.
"""

import json

from django.core.management.base import BaseCommand

from brands.models.brand_files import BrandFile
from brands.models.brand_online import BrandOnlineCredential
from brands.models.brands import Brand
from cloud_storage_loader.helpers import (
    make_logos_public,
    get_brand_category,
    get_brand_type,
    get_brand_online_url,
)
from tractors_be.settings import (
    CLOUD_STORAGE_CLIENT,
    GS_BUCKET_NAME,
    CLOUD_STORAGE_ROOT_FOLDER_NAME,
    CLOUD_STORAGE_BUCKET_INSTANCE,
)


class Command(BaseCommand):
    help = "Import all brands from CLoud Storage to the database"

    def handle(self, *args, **options):
        # 1. Remove all previous brands from the database
        self.stdout.write("Removing all previous brands from the database...")

        BrandFile.objects.all().delete()
        BrandOnlineCredential.objects.all().delete()
        Brand.objects.all().delete()

        self.stdout.write("All previous brands have been removed from the database.")

        # 2. Get all files in format: "CLOUD_STORAGE_ROOT_FOLDER_NAME/brand_name/..."
        self.stdout.write("Importing brands from Cloud Storage to the database...")

        all_files = [
            # 'gs://' + blob.id[:-(len(str(blob.generation)) + 1)]
            blob.name
            for blob in CLOUD_STORAGE_CLIENT.list_blobs(
                GS_BUCKET_NAME, prefix=CLOUD_STORAGE_ROOT_FOLDER_NAME
            )
            if (
                blob.name.endswith(".pdf")
                or blob.name.endswith(".zip")
                or blob.name.endswith(".json")
                or blob.name.endswith(".png")
            )
        ]

        # 3. Make public all logo files (needed to minimize the number of requests to the server front-end side)
        make_logos_public(all_files)
        self.stdout.write("All logo files are public now.")

        # 4. Get all brands by files
        all_brands = list(set([file.split("/")[1] for file in all_files]))

        # 5. Group files by brand
        files_by_brand = {}

        for brand in all_brands:
            files_by_brand[brand] = [
                file for file in all_files if file.split("/")[1] == brand
            ]

        # 6. Populate 'Brands'
        self.stdout.write("Populating 'Brands'...")

        for brand in all_brands:
            Brand.objects.create(
                name=brand,
                image=CLOUD_STORAGE_BUCKET_INSTANCE.blob(
                    f"{CLOUD_STORAGE_ROOT_FOLDER_NAME}/{brand}/logo.png"
                ).public_url,
                category=get_brand_category(brand_files=files_by_brand[brand]),
                type=get_brand_type(brand_files=files_by_brand[brand]),
                brand_online_url=get_brand_online_url(
                    brand_files=files_by_brand[brand]
                ),
            )

        self.stdout.write("All brands have been imported to the database.")

        # 7. Populate 'BrandFiles'
        self.stdout.write("Populating 'BrandFiles'...")

        for brand in all_brands:
            for file in files_by_brand[brand]:
                if file.endswith(".pdf") or file.endswith(".zip"):
                    BrandFile.objects.create(
                        brand=Brand.objects.get(name=brand),
                        file=file,
                    )

        self.stdout.write("All brand files have been imported to the database.")

        # 8. Populate 'BrandOnlineCredentials'
        self.stdout.write("Populating 'BrandOnlineCredentials'...")

        for brand in all_brands:
            # Find if online credentials are available for a brand
            online_credential_files = [
                brand_file
                for brand_file in files_by_brand[brand]
                if brand_file.endswith("online-credentials.json")
            ]

            # There is only one online credential file
            if len(online_credential_files) == 1:
                credential_file_blob = [
                    blob
                    for blob in CLOUD_STORAGE_CLIENT.list_blobs(
                        GS_BUCKET_NAME, prefix=online_credential_files[0]
                    )
                    if blob.name == online_credential_files[0]
                ][0]

                credential_file: object = json.loads(
                    credential_file_blob.download_as_string()
                )

                online_credentials = credential_file["credentials"]

                for online_credential in online_credentials:
                    BrandOnlineCredential.objects.create(
                        brand=Brand.objects.get(name=brand),
                        username=online_credential["username"],
                        password=online_credential["password"],
                    )

        self.stdout.write(
            "All brand online credentials have been imported to the database."
        )
