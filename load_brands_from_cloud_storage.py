"""
Init brands
"""

import json

from cloud_storage_loader.helpers import (
    get_brand_category,
    get_brand_type,
    get_brand_online_url,
)
from tractors_be.settings import (
    CLOUD_STORAGE_CLIENT,
    CLOUD_STORAGE_BUCKET_INSTANCE,
    GS_BUCKET_NAME,
)

BRANDS_ROOT_FOLDER_NAME = "available-brands"
"""
Base folder which will contains all brands (in our case static/uploads)
"""

# @TODO: Take it from env
FIXTURE_FOLDER = "./brands/fixtures"
"""
Folder which will contains fixtures of brands and brand files
"""


if __name__ == "__main__":
    # 1. Get all files in format: "BRANDS_ROOT_FOLDER_NAME/brand_name/..."

    all_files = [
        # 'gs://' + blob.id[:-(len(str(blob.generation)) + 1)]
        blob.name
        for blob in CLOUD_STORAGE_CLIENT.list_blobs(
            GS_BUCKET_NAME, prefix=BRANDS_ROOT_FOLDER_NAME
        )
        if (
            blob.name.endswith(".pdf")
            or blob.name.endswith(".zip")
            or blob.name.endswith(".json")
            or blob.name.endswith(".png")
        )
    ]

    # Make public all logo files (needed to minimize the number of requests to the server)
    for file in all_files:
        if file.endswith("logo.png"):
            blob = CLOUD_STORAGE_BUCKET_INSTANCE.blob(file)
            blob.make_public()

    # 2. Get all brands by files

    all_brands = list(set([file.split("/")[1] for file in all_files]))

    # 3. Group files by brand
    files_by_brand = {}

    for brand in all_brands:
        files_by_brand[brand] = [
            file for file in all_files if file.split("/")[1] == brand
        ]

    # 4. Create fixtures - Brands

    json_brands_fixture = [
        {
            "model": "brands.Brand",
            "fields": {
                "name": brand,
                # Image of brand is public (we made it public in the previous step)
                "image": CLOUD_STORAGE_BUCKET_INSTANCE.blob(
                    f"{BRANDS_ROOT_FOLDER_NAME}/{brand}/logo.png"
                ).public_url,
                "category": get_brand_category(brand_files=files_by_brand[brand]),
                "type": get_brand_type(brand_files=files_by_brand[brand]),
                "brand_online_url": get_brand_online_url(
                    brand_files=files_by_brand[brand],
                ),
            },
        }
        for brand in all_brands
    ]

    with open(f"{FIXTURE_FOLDER}/brands.json", "w+") as brands_file:
        brands_file.write(json.dumps(json_brands_fixture, indent=4))
        print(f"Brands fixtures exported in {FIXTURE_FOLDER}/brands.json")

    # 5. Create fixtures - Brand files

    json_brand_files_fixture = []

    for brand in all_brands:
        json_brand_files_fixture = json_brand_files_fixture + [
            {
                "model": "brands.BrandFile",
                "fields": {
                    "brand": brand,
                    "file": file,
                },
            }
            for file in files_by_brand[brand]
            if file.endswith(".pdf") or file.endswith(".zip")
        ]

    with open(f"{FIXTURE_FOLDER}/brand_files.json", "w+") as brand_files_file:
        brand_files_file.write(json.dumps(json_brand_files_fixture, indent=4))
        print(f"Brand files fixtures exported in {FIXTURE_FOLDER}/brand_files.json")

    # 6. Create fixtures - Brand online credentials

    json_brand_online_credentials_fixture = []

    for brand in all_brands:
        online_credential_files = [
            brand_file
            for brand_file in files_by_brand[brand]
            if brand_file.endswith("online-credentials.json")
        ]

        if len(online_credential_files) == 1:
            credential_file_blob = [
                blob
                for blob in CLOUD_STORAGE_CLIENT.list_blobs(
                    "tractors", prefix=online_credential_files[0]
                )
                if blob.name == online_credential_files[0]
            ][0]

            credential_file: object = json.loads(
                credential_file_blob.download_as_string()
            )

            online_credentials = credential_file["credentials"]

            json_brand_online_credentials_fixture = (
                json_brand_online_credentials_fixture
                + [
                    {
                        "model": "brands.BrandOnlineCredential",
                        "fields": {
                            "brand": brand,
                            "username": online_credential["username"],
                            "password": online_credential["password"],
                        },
                    }
                    for online_credential in online_credentials
                ]
            )

    with open(
        f"{FIXTURE_FOLDER}/brand_online_credentials.json", "w+"
    ) as brand_credentials_file:
        brand_credentials_file.write(
            json.dumps(json_brand_online_credentials_fixture, indent=4)
        )
        print(
            f"Brands credentials fixtures exported in {FIXTURE_FOLDER}/brands_files.json"
        )
