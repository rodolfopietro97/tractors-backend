"""
Views for the customer's app
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Customer
from .serializers import CustomerSerializer, CustomerUpdateSerializer


class CheckCustomerRegistration(generics.GenericAPIView):
    """
    Check if the customer has completed the registration process
    """

    permission_classes = [IsAuthenticated]
    queryset = Customer.objects.all()

    def get(self, request, *args, **kwargs):
        """
        Check if the customer has completed the registration process
        :param request: Request object
        :param args: Additional arguments
        :param kwargs: Keyword arguments
        :return: If the customer has completed the registration process or not
        """
        exists = False
        try:
            exists = Customer.objects.filter(user=self.request.user).exists()
        except:
            exists = False

        return Response({"customer_completed_registration": exists})


class CreateCustomer(generics.CreateAPIView):
    """
    Create a new customer
    """

    permission_classes = [IsAuthenticated]

    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    # Create Customer
    def perform_create(self, serializer):
        # Passo il parametro extra 'user' al serializer
        return serializer.save(user=self.request.user)

    # Viene chiamato prima di perform_create, controllo se il client è già registrato
    def create(self, request, *args, **kwargs):
        register_set = Customer.objects.filter(user=self.request.user)
        if register_set.exists():
            return Response({"user": ["Customer already signed up"]}, status=400)

        try:
            # Crate the customer
            super().create(request, *args, **kwargs)

            # Return the response
            return Response({"status": "ok"}, status=200)
        except:
            return Response({"status": "error"}, status=400)


class UpdateCustomer(generics.UpdateAPIView):
    """
    Update an existing customer
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CustomerUpdateSerializer

    def get_object(self):
        return Customer.objects.get(user=self.request.user.pk)

    def perform_update(self, serializer: CustomerUpdateSerializer):
        return super().perform_update(serializer)


class RetrieveCustomer(generics.RetrieveAPIView):
    """
    Retrieve an existing customer
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer

    def get_object(self):
        return Customer.objects.get(user=self.request.user.pk)
