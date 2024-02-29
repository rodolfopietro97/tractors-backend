"""
Serializers for the Customers model.
"""

from rest_framework import serializers

from .models import Customer


class CustomerUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model used for updates
    """

    class Meta:
        exclude = ["user"]
        model = Customer


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model
    """

    class Meta:
        exclude = ["user"]
        model = Customer
