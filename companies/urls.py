"""
Urls for the companies' app
"""

from django.urls import path

from .views import (
    CreateCompany,
    CheckCompanyRegistration,
    RetrieveCompany,
    UpdateCompany,
)

urlpatterns = [
    path(
        "check-company-registration/",
        CheckCompanyRegistration.as_view(),
        name="check-company-registration",
    ),
    path("create-company/", CreateCompany.as_view(), name="create-company"),
    path("update-company/", UpdateCompany.as_view(), name="update-company"),
    path("get-company/", RetrieveCompany.as_view(), name="get-company"),
]
