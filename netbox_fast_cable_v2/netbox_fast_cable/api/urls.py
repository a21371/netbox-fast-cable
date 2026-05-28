from django.urls import path
from netbox_fast_cable import views

urlpatterns = [
    path("devices/", views.list_devices),
    path("interfaces/<int:device_id>/", views.list_interfaces),
    path("create-cable/", views.create_cable),
]
