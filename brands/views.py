"""
Views for brands' app.
"""

import datetime
import json
import random

from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from tractors_be.settings import CLOUD_STORAGE_BUCKET_INSTANCE
from .brand_fetch_strategy.fetch_map import fetch_brand
from .models.brand_files import BrandFile
from .models.brand_online import BrandOnlineCredential
from .models.brands import Brand
from .serializers import BrandSerializer, BrandFileSerializer


class AllBrandsList(generics.ListAPIView):
    """
    View to list all brands in the system.
    """

    permission_classes = [AllowAny]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class AllBrandFilesListFilteredByBrandName(generics.ListAPIView):
    """
    View to list all brand files in the system filtered by brand.
    """

    lookup_url_kwarg = "brand_name"
    permission_classes = [IsAuthenticated]
    serializer_class = BrandFileSerializer

    def get_queryset(self):
        brand_name = self.kwargs.get(self.lookup_url_kwarg)
        return BrandFile.objects.filter(brand=brand_name)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def online_brand_authentication_parameters(request, brand_name, format=None):
    """
    Get credentials for online brand authentication parameters given brand name.
    @TODO handle errors
    """
    if request.method == "GET":
        # Get brand url
        brand = Brand.objects.get(name=brand_name)

        # Get all brands credentials
        brands_credentials_filtered_by_name = BrandOnlineCredential.objects.filter(
            brand=brand_name
        )
        all_credentials_available_for_a_brand = [
            credential for credential in brands_credentials_filtered_by_name.values()
        ]

        # No credentials available for a brand
        if len(all_credentials_available_for_a_brand) == 0:
            return Response({"url": brand.brand_online_url}, status=status.HTTP_200_OK)

        # Get random credentials from all credentials available for a brand
        selected_credentials = all_credentials_available_for_a_brand[
            random.randint(0, len(all_credentials_available_for_a_brand) - 1)
        ]

        # Get tokens and all stuff needed for online authentication in brand site here
        # @NOTE: OLD code to retrieve authentication parameters from Landini website.
        # Currently not used because the method doesn't work.

        # final_response = fetch_brand(
        #     brand_name=brand_name,
        #     credentials={
        #         'username': selected_credentials['username'],
        #         'password': selected_credentials['password'],
        #     },
        #     headers=request.headers
        # )

        response = Response(
            {
                "url": brand.brand_online_url,
                "credentials": {
                    "username": selected_credentials["username"],
                    "password": selected_credentials["password"],
                },
            },
            status=status.HTTP_200_OK,
        )
        # response.set_cookie(key='brand_name', value=brand_name, domain='pippo.com')

        return response


@api_view(["GET"])
def online_brand_authentication_parameters2(request, brand_name, format=None):
    if request.method == "GET":
        # Get brand url
        brand = Brand.objects.get(name=brand_name)

        brands_credentials_filtered_by_name = BrandOnlineCredential.objects.filter(
            brand=brand_name
        )
        all_credentials_available_for_a_brand = [
            credential for credential in brands_credentials_filtered_by_name.values()
        ]

        selected_credentials = all_credentials_available_for_a_brand[
            random.randint(0, len(all_credentials_available_for_a_brand) - 1)
        ]
        print(selected_credentials)

        final_response = fetch_brand(
            brand_name=brand_name,
            credentials={
                "username": selected_credentials["username"],
                "password": selected_credentials["password"],
            },
            headers=request.headers,
        )
        print(final_response)

        res = Response({"ciccio": "a"})

        return Response(
            {
                "session_storage": {
                    "injenia-argotractors-authportalcrm-session-access-token": final_response[
                        "session_storage"
                    ][
                        "injenia-argotractors-authportalcrm-session-access-token"
                    ],
                    "injenia-argotractors-authportalportal_language": final_response[
                        "session_storage"
                    ]["injenia-argotractors-authportalportal_language"],
                    "injenia-argotractors-authportalportal_language_code": final_response[
                        "session_storage"
                    ][
                        "injenia-argotractors-authportalportal_language_code"
                    ],
                    "injenia-argotractors-authportalportal_brand": final_response[
                        "session_storage"
                    ]["injenia-argotractors-authportalportal_brand"],
                    "injenia-argotractors-authportalsession-access-token": final_response[
                        "session_storage"
                    ][
                        "injenia-argotractors-authportalsession-access-token"
                    ],
                }
            }
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def get_private_file_url(request, format=None):
    """
    Get file url given file name.
    """
    if request.method == "POST":
        # Get file url
        requestBody = json.loads(request.body.decode("utf-8"))
        file_path = requestBody["file_path"]

        if CLOUD_STORAGE_BUCKET_INSTANCE.blob(file_path).exists():
            signed_url = CLOUD_STORAGE_BUCKET_INSTANCE.blob(
                file_path
            ).generate_signed_url(
                version="v4",
                # This URL is valid for 15 minutes
                expiration=datetime.timedelta(seconds=15),
                # Allow 'GET' requests using this URL.
                method="GET",
            )

            return Response(
                signed_url,
                status=status.HTTP_200_OK,
            )

        return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)
