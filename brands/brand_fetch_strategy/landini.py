"""
Fetch strategy for Landini brand.

Goal: Login on https://gate.argotractors.com/portal/index.html#/login
Steps:
1. Get access token from https://gate.argotractors.com/portal/api/core/auth/create-access-token-by-credentials
2. Get CRM Dashboard access token from https://gate.argotractors.com/portal/api/core/auth/create-crm-access-token-by-credentials (use access token from step 1 as Bearer token)
3. Give back final response:
```
{
            'session_storage': {
                'injenia-argotractors-authportalcrm-session-access-token': crm_access_token,
                'injenia-argotractors-authportalportal_language': 'ITA',
                'injenia-argotractors-authportalportal_language_code': 1,
                'injenia-argotractors-authportalportal_brand': 'argo',
                'injenia-argotractors-authportalsession-access-token': access_token,
            }
}
```
"""

import requests

PORTAL_ACCESS_TOKEN_URL = "https://gate.argotractors.com/portal/api/core/auth/create-access-token-by-credentials"
"""
URL to get access token from Landini website.
"""

CRM_ACCESS_TOKEN_URL = "https://gate.argotractors.com/portal/api/core/auth/create-crm-access-token-by-credentials"
"""
URL to get CRM Dashboard access token from Landini website.
"""


def fetch_brand_data_landini(credentials: dict, headers: dict):
    """
    Fetch brand data strategy from Landini website.

    :param credentials: credentials to authenticate on website
    :param headers: headers from request

    :return: dict with credentials tokens needed to authenticate on website
    """
    # 1. Get access token
    headers_access_token_request = {
        "authority": "gate.argotractors.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "it-IT,it;q=0.7",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://gate.argotractors.com",
        "referer": "https://gate.argotractors.com/portal/index.html",
        "sec-ch-ua": headers["Sec-Ch-Ua"],
        "sec-ch-ua-mobile": headers["Sec-Ch-Ua-Mobile"],
        "sec-ch-ua-platform": headers["Sec-Ch-Ua-Platform"],
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": headers["Sec-Gpc"],
        "user-agent": headers["User-Agent"],
    }

    response_access_token = requests.post(
        PORTAL_ACCESS_TOKEN_URL,
        headers=headers_access_token_request,
        json=credentials,
    ).json()
    access_token = response_access_token["accessToken"]

    # 2. Get CRM Dashboard access token
    headers_crm_dashboard = {
        "authority": "gate.argotractors.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "it-IT,it;q=0.7",
        "authorization": f"Bearer {access_token}",
        # 'content-length': '0',
        "origin": "https://gate.argotractors.com",
        "referer": "https://gate.argotractors.com/portal/index.html",
        "sec-ch-ua": headers["Sec-Ch-Ua"],
        "sec-ch-ua-mobile": headers["Sec-Ch-Ua-Mobile"],
        "sec-ch-ua-platform": headers["Sec-Ch-Ua-Platform"],
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": headers["Sec-Gpc"],
        "user-agent": headers["User-Agent"],
    }

    response_crm_token = requests.post(
        CRM_ACCESS_TOKEN_URL,
        headers=headers_crm_dashboard,
    ).json()
    crm_access_token = response_crm_token["accessToken"]

    # 3. Give back final response
    return {
        "session_storage": {
            "injenia-argotractors-authportalcrm-session-access-token": crm_access_token,
            "injenia-argotractors-authportalportal_language": "ITA",
            "injenia-argotractors-authportalportal_language_code": 1,
            "injenia-argotractors-authportalportal_brand": "argo",
            "injenia-argotractors-authportalsession-access-token": access_token,
        }
    }
