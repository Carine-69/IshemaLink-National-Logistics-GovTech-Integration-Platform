"""
URL configuration for ishemalink_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin
from django.urls import path
from Core.views import create_shipment_view, payment_webhook_view
import random
from django.db import models

@csrf_exempt
def api_root(request):
    return JsonResponse({
        "name": "IshemaLink API",
        "version": "v1"
    })

@csrf_exempt
def health_check(request):
    return JsonResponse({
        "status": "ok",
        "database": "connected"
    })

@csrf_exempt
def tracking_live_view(request, shipment_id):
    # Simulate real-time coordinates (in production, fetch from GPS or DB)
    coords = {
        "lat": round(-1.95 + random.uniform(-0.05, 0.05), 6),
        "lng": round(30.06 + random.uniform(-0.05, 0.05), 6),
        "shipment_id": shipment_id
    }
    return JsonResponse(coords)

@csrf_exempt
def notifications_broadcast_view(request):
    if request.method == 'POST':
        from Core.models import Driver
        from notifications import NotificationEngine
        notifier = NotificationEngine()
        drivers = Driver.objects.all()
        message = request.GET.get('message', 'Admin broadcast to all drivers')
        for driver in drivers:
            notifier.send_sms(driver.phone_number, message)
        return JsonResponse({"status": "broadcast sent", "driver_count": drivers.count()})
    return JsonResponse({"error": "Invalid method"}, status=405)

@csrf_exempt
def admin_dashboard_summary_view(request):
    from Core.models import Shipment, Driver
    active_trucks = Shipment.objects.filter(status="confirmed").count()
    total_revenue = Shipment.objects.filter(status="confirmed").aggregate(total=models.Sum('tariff'))['total'] or 0
    available_drivers = Driver.objects.filter(is_available=True).count()
    return JsonResponse({
        "active_trucks": active_trucks,
        "total_revenue": total_revenue,
        "available_drivers": available_drivers
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api_root),
    path("api/status/", health_check),
    path("api/shipments/create/", create_shipment_view),
    path("api/payments/webhook/", payment_webhook_view),
    path("tracking/<int:shipment_id>/live/", tracking_live_view),
    path("notifications/broadcast/", notifications_broadcast_view),
    path("dashboard/summary/", admin_dashboard_summary_view),
    path("dashboard/",  __import__('Core.views', fromlist=['dashboard_html_view']).dashboard_html_view),
    path("analytics/routes/top/", __import__('Core.views', fromlist=['analytics_routes_top_view']).analytics_routes_top_view),
    path("analytics/commodities/breakdown/", __import__('Core.views', fromlist=['analytics_commodities_breakdown_view']).analytics_commodities_breakdown_view),
    path("analytics/revenue/heatmap/", __import__('Core.views', fromlist=['analytics_revenue_heatmap_view']).analytics_revenue_heatmap_view),
    path("analytics/drivers/leaderboard/", __import__('Core.views', fromlist=['analytics_drivers_leaderboard_view']).analytics_drivers_leaderboard_view),
    path("gov/ebm/sign-receipt/", __import__('Core.views', fromlist=['gov_ebm_sign_receipt_view']).gov_ebm_sign_receipt_view),
    path("gov/rura/verify-license/<str:license_no>/", __import__('Core.views', fromlist=['gov_rura_verify_license_view']).gov_rura_verify_license_view),
    path("gov/customs/generate-manifest/", __import__('Core.views', fromlist=['gov_customs_generate_manifest_view']).gov_customs_generate_manifest_view),
    path("gov/audit/access-log/", __import__('Core.views', fromlist=['gov_audit_access_log_view']).gov_audit_access_log_view),
]