"""
Urls for the customer's app.
"""

from django.urls import path

from .views import (
    CheckCustomerRegistration,
    CreateCustomer,
    RetrieveCustomer,
    UpdateCustomer,
)

urlpatterns = [
    path(
        "check-customer-registration/",
        CheckCustomerRegistration.as_view(),
        name="check-customer-registration",
    ),
    path("create-customer/", CreateCustomer.as_view(), name="create-customer"),
    path("update-customer/", UpdateCustomer.as_view(), name="update-customer"),
    path("get-customer/", RetrieveCustomer.as_view(), name="get-customer"),
]
