from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from dashboard.models import Notification
from django.utils.translation import gettext as _

@login_required
@require_GET
def get_notifications(request):
    notifications = Notification.objects.filter(user=request.user)
    if notifications:
        return JsonResponse({
            "notifications": [
                {
                    "id": n.id,
                    "title": n.title,
                    "message": n.message,
                    "created_at": n.created_at.isoformat(),
                    "is_read": n.is_read,
                } for n in notifications
            ]
        })
    else:
        return JsonResponse({"error": _("No notifications found")})

@login_required
@require_POST
def set_read(request):
    try:
        # Get count before update
        unread_count = Notification.objects.filter(
            user=request.user, 
            is_read=False
        ).count()
        
        if unread_count == 0:
            return JsonResponse({
                "success": True,
                "message": _("All notifications are already marked as read"),
                "updated_count": 0
            })
            
        # Update unread notifications
        updated = Notification.objects.filter(
            user=request.user, 
            is_read=False
        ).update(is_read=True)
        
        return JsonResponse({
            "success": True,
            "message": _("Successfully marked {} notifications as read").format(updated) if updated > 1 
                        else _("Successfully marked 1 notification as read"),
            "updated_count": updated
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            "success": False,
            "message": _("An error occurred while updating notifications"),
            "error": str(e),
            "details": "Please try again later or contact support if the problem persists."
        }, status=500)
