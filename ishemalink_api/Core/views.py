from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from Core.booking_service import BookingService
from payments import MomoMock
from notifications import NotificationEngine
from Core.models import Shipment, Driver
from django.db import models

# Dependency injection
payment_gateway = MomoMock()
notifier = NotificationEngine()
booking_service = BookingService(payment_gateway, notifier)

@csrf_exempt
def create_shipment_view(request):
    if request.method == 'POST':
        try:
            raw_body = request.body.decode('utf-8')
            print('Raw request body:', raw_body)
            if not raw_body:
                return JsonResponse({'error': 'Empty request body'}, status=400)
            data = json.loads(raw_body)
            result = booking_service.create_shipment(data)
            return JsonResponse(result, status=201)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def payment_webhook_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            booking_service.handle_payment_callback(data)
            return JsonResponse({'status': 'callback processed'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def dashboard_html_view(request):
    active_trucks = Shipment.objects.filter(status="confirmed").count()
    total_revenue = Shipment.objects.filter(status="confirmed").aggregate(total=models.Sum('tariff'))['total'] or 0
    available_drivers = Driver.objects.filter(is_available=True).count()
    return render(request, "dashboard.html", {
        "active_trucks": active_trucks,
        "total_revenue": total_revenue,
        "available_drivers": available_drivers
    })

@csrf_exempt
def analytics_routes_top_view(request):
    data = [
        {"route": "Kigali - Musanze", "count": 120},
        {"route": "Kigali - Huye", "count": 95},
        {"route": "Kigali - Rubavu", "count": 80},
        {"route": "Kigali - Rusizi", "count": 60},
        {"route": "Kigali - Nyagatare", "count": 50}
    ]
    return JsonResponse({"top_routes": data})

@csrf_exempt
def analytics_commodities_breakdown_view(request):
    data = [
        {"commodity": "Potatoes", "volume": 20000},
        {"commodity": "Electronics", "volume": 8000},
        {"commodity": "Beans", "volume": 5000}
    ]
    return JsonResponse({"commodities": data})

@csrf_exempt
def analytics_revenue_heatmap_view(request):
    data = [
        {"sector": "Kicukiro", "revenue": 5000000},
        {"sector": "Gasabo", "revenue": 4000000},
        {"sector": "Nyarugenge", "revenue": 3500000}
    ]
    return JsonResponse({"revenue_heatmap": data})

@csrf_exempt
def analytics_drivers_leaderboard_view(request):
    data = [
        {"driver": "Jean Bosco", "on_time_deliveries": 45},
        {"driver": "Alice Uwase", "on_time_deliveries": 40},
        {"driver": "Eric Nshimiyimana", "on_time_deliveries": 38}
    ]
    return JsonResponse({"leaderboard": data})

@csrf_exempt
def gov_ebm_sign_receipt_view(request):
    # Simulate EBM signature
    import uuid
    data = json.loads(request.body)
    return JsonResponse({
        "receipt_id": str(uuid.uuid4()),
        "signature": "EBM-MOCK-SIGNATURE",
        "amount": data.get("amount"),
        "timestamp": data.get("timestamp")
    })

@csrf_exempt
def gov_rura_verify_license_view(request, license_no):
    # Simulate license check
    valid = license_no.startswith("RWA")
    return JsonResponse({
        "license_no": license_no,
        "valid": valid,
        "status": "active" if valid else "invalid"
    })

@csrf_exempt
def gov_customs_generate_manifest_view(request):
    # Simulate EAC-compliant XML manifest
    manifest_xml = """<Manifest><ShipmentID>12345</ShipmentID><Status>Generated</Status></Manifest>"""
    return JsonResponse({"manifest": manifest_xml})

@csrf_exempt
def gov_audit_access_log_view(request):
    # Simulate audit log
    logs = [
        {"user": "admin", "action": "viewed shipment", "timestamp": "2026-02-17T10:00:00Z"},
        {"user": "officer", "action": "verified license", "timestamp": "2026-02-17T11:00:00Z"}
    ]
    return JsonResponse({"audit_log": logs})

# Create your views here.
