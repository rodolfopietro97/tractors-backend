"""
Fetch strategy for Valpadana brand.

... SAME OF LANDINI ...

"""

from brands.brand_fetch_strategy.landini import fetch_brand_data_landini


def fetch_brand_data_valpadana(credentials: dict, headers: dict):
    """
    Fetch brand data strategy from Valpadana website.

    :param credentials: credentials to authenticate on website
    :param headers: headers from request

    :return: dict with credentials tokens needed to authenticate on website
    """
    return fetch_brand_data_landini(credentials=credentials, headers=headers)
