from django.urls import path
from . import views

urlpatterns = [
    path("form/", views.contacts_form_view, name="contacts-form-email"),
]
