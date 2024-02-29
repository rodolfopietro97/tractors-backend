"""
Correct fetch brand strategy function depending on brand name.
"""

from brands.brand_fetch_strategy.landini import fetch_brand_data_landini
from brands.brand_fetch_strategy.mccormick import fetch_brand_data_mccormick
from brands.brand_fetch_strategy.valpadana import fetch_brand_data_valpadana


def fetch_brand(brand_name: str, credentials: dict, headers: dict):
    """
    Fetch brand data strategy from website.

    :param brand_name: brand name
    :param credentials: credentials to authenticate on website
    :param headers: headers from request

    :return: dict with credentials tokens needed to authenticate on website
    """
    if brand_name.lower() == "landini":
        return fetch_brand_data_landini(credentials=credentials, headers=headers)
    elif brand_name.lower() == "mccormick":
        return fetch_brand_data_mccormick(credentials=credentials, headers=headers)
    elif brand_name.lower() == "valpadana":
        return fetch_brand_data_valpadana(credentials=credentials, headers=headers)
    else:
        return {
            "error": "Brand not found",
        }
