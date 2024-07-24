from django.urls import path

from . import api

urlpatterns = [
    path("", api.property_list, name="api_properties_list"),
    path("create/", api.create_property, name="api_create_property"),
    path("<uuid:pk>/", api.properties_detail, name="api_properties_detail"),
]
