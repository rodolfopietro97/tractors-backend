"""
Views for the companies' app
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Company
from .serializers import CompanySerializer, CompanyUpdateSerializer


class CheckCompanyRegistration(generics.GenericAPIView):
    """
    Check if the company has completed the registration process
    """

    permission_classes = [IsAuthenticated]
    queryset = Company.objects.all()

    def get(self, request, *args, **kwargs):
        """
        Check if the company has completed the registration process
        :param request: Request object
        :param args: Arguments
        :param kwargs: Keyword arguments
        :return: If the company has completed the registration process
        """
        exists = False
        try:
            exists = Company.objects.filter(user=self.request.user).exists()
        except Exception:
            exists = False

        return Response({"company_completed_registration": exists})


class CreateCompany(generics.CreateAPIView):
    """
    Create a new company
    """

    permission_classes = [IsAuthenticated]

    serializer_class = CompanySerializer
    queryset = Company.objects.all()

    # Create CompanySerializer
    def perform_create(self, serializer):
        """
        Perform the creation of the company
        :param serializer: Serializer to use
        :return: Perform the creation of the company
        """
        # Extract the user from the request and save it in the serializer
        return serializer.save(user=self.request.user)

    # Viene chiamato prima di perform_create, controllo se il client è già registrato
    def create(self, request, *args, **kwargs):
        """
        Create a new company
        :param request: Request object
        :param args: Arguments
        :param kwargs: Keyword arguments
        :return: Create a new company
        """
        register_set = Company.objects.filter(user=self.request.user)
        if register_set.exists():
            return Response({"company": ["Company already exists"]}, status=400)

        try:
            super().create(request, *args, **kwargs)
            return Response({"status": "ok"}, status=200)
        except Exception:
            return Response({"status": "error"}, status=400)


class UpdateCompany(generics.UpdateAPIView):
    """
    Update an existing customer
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CompanyUpdateSerializer

    def get_object(self):
        """
        Get the company object
        :return: Company object
        """
        return Company.objects.get(user=self.request.user.pk)

    def perform_update(self, serializer: CompanyUpdateSerializer):
        """
        Perform the update of the company
        :param serializer: Serializer to use
        :return: Perform the update of the company
        """
        return super().perform_update(serializer)


class RetrieveCompany(generics.RetrieveAPIView):
    """
    Retrieve an existing company
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CompanySerializer

    def get_object(self):
        """
        Get the company object
        :return: Company object
        """
        return Company.objects.get(user=self.request.user.pk)
