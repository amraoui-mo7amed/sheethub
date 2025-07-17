from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from frontend.models import Order
import json

@csrf_exempt
@require_POST
def update_order_status(request):
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": _("Authentication required")}, status=401)

    try:
        data = json.loads(request.body)
        order_id = data.get("order_id")
        new_status = data.get("status")

        order = Order.objects.select_related("product").get(id=order_id)

        # Ensure current user owns the product
        if order.product.user != request.user:
            return JsonResponse({"success": False, "message": _("You are not authorized to perform this action")}, status=403)

        # Validate status
        valid_statuses = [choice[0] for choice in order.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return JsonResponse({"success": False,  "message": _("Invalid status value")}, status=400)

        order.status = new_status
        order.save()

        return JsonResponse({
            "success": True,
            'success_title': _("Updated"),
            "message": _("Order status updated successfully"),
            "order_id": order.id,
            "new_status": order.status
        })

    except Order.DoesNotExist:
        return JsonResponse({"success": False, "message": _("Order not found")}, status=404)

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)
