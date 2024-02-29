"""
Helper functions for cloud-storage-loader of brands
"""

import json

from tractors_be.settings import CLOUD_STORAGE_CLIENT, GS_BUCKET_NAME


def get_brand_category(brand_files: list) -> str:
    """
    Get category of brand
    :brand_files: Input brand_files grouped for brand name
    :return: "Attrezzature", "Trattori" or "Entrambi"
    """

    # Filter files by brand name
    attrezzature = False
    trattori = False

    for file in brand_files:
        if "/Attrezzature" in file:
            attrezzature = True

        if "/Trattori" in file:
            trattori = True

    # Only "Attrezzature"
    if attrezzature and not trattori:
        return "Attrezzature"

    # Only "Trattori"
    if trattori and not attrezzature:
        return "Trattori"

    return "Entrambi"


def get_brand_type(brand_files: list) -> str:
    """
    Get type of brand
    :brand_files: Input brand_files grouped for brand name
    :return: "Online", "PDF" or "Entrambi"
    """

    # 1 - Find if is a PDF brand. Attrezzature or Trattori folder NOT empty

    is_pdf_brand = False

    count_attrezzature = len([file for file in brand_files if "/Attrezzature" in file])

    count_trattori = len([file for file in brand_files if "/Trattori" in file])

    if count_attrezzature > 0 or count_trattori > 0:
        is_pdf_brand = True

    # 2 - Find if online credentials are available for a brand

    is_online_brand = (
        len(
            [
                brand_file
                for brand_file in brand_files
                if brand_file.endswith("online-credentials.json")
            ]
        )
        > 0
    )

    return (
        "Entrambi"
        if is_pdf_brand and is_online_brand
        else "PDF" if is_pdf_brand else "Online"
    )


def get_brand_online_url(brand_files: list) -> str or None:
    """
    Get url of brand online (if exists)
    :brand_files: Input brand_files grouped for brand name
    :return: url of online brand
    """

    # 1 - Find if online credentials are available for a brand

    is_online_brand = (
        len(
            [
                brand_file
                for brand_file in brand_files
                if brand_file.endswith("online-credentials.json")
            ]
        )
        > 0
    )

    if is_online_brand:
        credential_file = [
            brand_file
            for brand_file in brand_files
            if brand_file.endswith("online-credentials.json")
        ][0]

        credential_file_blob = [
            blob
            for blob in CLOUD_STORAGE_CLIENT.list_blobs(
                GS_BUCKET_NAME, prefix=credential_file
            )
            if blob.name == credential_file
        ][0]

        credential_file: object = json.loads(credential_file_blob.download_as_string())

        return credential_file["url"]

    return None
