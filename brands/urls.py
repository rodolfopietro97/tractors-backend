from django.urls import path

from . import views

urlpatterns = [
    # Get all brands
    path("list/", views.AllBrandsList.as_view()),
    # Get all brand files filtered by brand name
    path("files/<brand_name>", views.AllBrandFilesListFilteredByBrandName.as_view()),
    # Get online brand authentication parameters given brand_name
    path("brand-online/<brand_name>", views.online_brand_authentication_parameters),
    path("brand-online2/<brand_name>", views.online_brand_authentication_parameters2),
    # Get file url
    path("file-signed-url/", views.get_private_file_url),
]
