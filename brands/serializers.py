from rest_framework import serializers

from .models.brand_files import BrandFile
from .models.brand_online import BrandOnlineCredential
from .models.brands import Brand


class BrandSerializer(serializers.ModelSerializer):
    """
    Serializer for Brand model.
    """

    class Meta:
        fields = ["name", "image", "category", "type", "brand_online_url"]
        model = Brand


class BrandFileSerializer(serializers.ModelSerializer):
    """
    Serializer for Brand File model.
    It gets all brand files
    """

    class Meta:
        fields = ["file", "brand", "description"]
        model = BrandFile


class BrandOnlineCredentialSerializer(serializers.ModelSerializer):
    """
    Serializer for Brand File model.
    It gets all brand files
    """

    class Meta:
        fields = ["username", "brand", "password"]
        model = BrandOnlineCredential
