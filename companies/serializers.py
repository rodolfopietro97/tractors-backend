"""
Serializers for the Company model
"""

from rest_framework import serializers

from .models import Company


class CompanyUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for the Company model used for updates
    """

    class Meta:
        exclude = ["user"]
        model = Company


class CompanySerializer(serializers.ModelSerializer):
    """
    Serializer for the Company model
    """

    class Meta:
        exclude = ["user"]
        model = Company
