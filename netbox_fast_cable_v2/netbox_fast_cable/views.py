from django.shortcuts import render
from django.http import JsonResponse
from dcim.models import Device, Interface, Cable
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
import json

def index(request):
    return render(request, "netbox_fast_cable/index.html", {})

def list_devices(request):
    devices = Device.objects.all().order_by("name")
    return JsonResponse({
        "devices": [{"id": d.id, "name": d.name} for d in devices]
    })

def list_interfaces(request, device_id):
    device = Device.objects.get(id=device_id)
    interfaces = Interface.objects.filter(device=device).order_by("name")

    return JsonResponse({
        "interfaces": [
            {
                "id": i.id,
                "name": i.name,
                "connected": i.cable is not None
            } for i in interfaces
        ]
    })

@require_POST
@csrf_protect
def create_cable(request):
    data = json.loads(request.body)

    a = Interface.objects.get(id=data["a"])
    b = Interface.objects.get(id=data["b"])

    if a == b:
        return JsonResponse({"error": "Cannot connect interface to itself"}, status=400)

    if a.cable or b.cable:
        return JsonResponse({"error": "One interface already has a cable"}, status=400)

    cable = Cable(
        termination_a_type=ContentType.objects.get_for_model(Interface),
        termination_a_id=a.id,
        termination_b_type=ContentType.objects.get_for_model(Interface),
        termination_b_id=b.id,
    )
    cable.save()

    return JsonResponse({"success": True, "cable_id": cable.id})
