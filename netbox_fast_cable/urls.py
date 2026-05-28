from django.urls import path, include
from . import views

app_name = "netbox_fast_cable"

urlpatterns = [
    path("", views.index, name="index"),
    path("api/", include("netbox_fast_cable.api.urls")),
]
