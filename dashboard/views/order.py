from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q
from dashboard.decorators import role_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from frontend.models import Order
from dashboard.models import Product
import json
from utils import loadJSON
from django.db.models import Sum, F

@login_required
@role_required(['seller'])
def list(request):
    context = {}
    wilayas = loadJSON('algeria.json')
    unique_wilayas = {(entry["wilaya_code"], entry["wilaya_name_ascii"]) for entry in wilayas}
    
    orders = Order.objects.filter(product__user=request.user)
    
    context.update({
        'wilaya_choices': unique_wilayas,
        'orders': orders,
        'products': [(product.pk, product.name) for product in Product.objects.filter(user=request.user)],
        'status_choices': [(k, v) for k, v in Order.STATUS_CHOICES],
        'pending_count': orders.filter(status='pending').count(),
        'delivered_count': orders.filter(status='delivered').count(),
        'total_revenue': orders.aggregate(
            total=Sum(F('quantity') * F('product__price'))
        )['total']
    })
    
    return render(request, 'orders/list.html', context=context)


@csrf_exempt
@require_POST
@login_required
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


@login_required
@role_required(['seller'])
@require_GET
def order_details(request, order_id):
    try:
        order = Order.objects.select_related("product").get(id=order_id, product__user=request.user)
        return JsonResponse({
            "success": True,
            "order": {
                "id": order.id,
                "full_name": order.full_name,
                "phone_number": order.phone_number,
                "wilaya": order.wilaya_display,  # Assuming wilaya_display is a property that returns the name
                "commune": order.commune,
                "product": {
                    "id": order.product.id,
                    "name": order.product.name,
                    "price": str(order.product.price),  # Convert to string for JSON serialization
                },
                "quantity": order.quantity,
                "status": order.get_status_display(),  # Get the human-readable status
                "total_price": str(order.total_price),  # Convert to string for JSON serialization
                "is_confirmed": order.is_confirmed,
                "created_at": order.created_at.isoformat(),
            }
        })
    except Order.DoesNotExist:
        return JsonResponse({"success": False, "message": _("Order not found")}, status=404)


@login_required
@role_required(['seller']) # Include your role check here if needed for this AJAX endpoint
def filter_orders_ajax(request):
    """
    Handles AJAX GET requests to filter orders based on various criteria
    provided by the frontend filter widget.
    Returns filtered order data as a JSON response.
    """
    # This check is technically redundant if @login_required works,
    # but good for clarity given the ongoing user issue.
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    # Start with orders belonging to the current user's products
    # .select_related('product') optimizes database queries
    orders = Order.objects.filter(product__user=request.user)

    # --- Get Filter Parameters from Request.GET ---
    # Map HTML input IDs to query parameters and clean input
    status_filter = request.GET.get('status', '').strip()
    product_name_filter = request.GET.get('product_name', '').strip()
    client_full_name_filter = request.GET.get('client_full_name', '').strip()
    client_phone_number_filter = request.GET.get('client_phone_number', '').strip()
    wilaya_filter = request.GET.get('wilaya', '').strip()
    commune_filter = request.GET.get('commune', '').strip()

    # --- Apply Filters Dynamically ---
    if status_filter:
        orders = orders.filter(status=status_filter)

    if product_name_filter:
        # Filter by product name (case-insensitive contains)
        orders = orders.filter(product__name__icontains=product_name_filter)

    if client_full_name_filter:
        # Filter by client full name (case-insensitive contains)
        orders = orders.filter(full_name__icontains=client_full_name_filter)

    if client_phone_number_filter:
        # Filter by client phone number (case-insensitive contains)
        orders = orders.filter(phone_number__icontains=client_phone_number_filter)

    if wilaya_filter:
        # Filter by wilaya name (case-insensitive contains)
        # Assuming your Order model has wilaya_name_ascii or similar for searching
        orders = orders.filter(Q(wilaya_name__icontains=wilaya_filter) | Q(wilaya_name_ascii__icontains=wilaya_filter))

    if commune_filter:
        # Filter by commune name (case-insensitive contains)
        orders = orders.filter(commune__icontains=commune_filter)

    # --- Prepare Data for JSON Response ---
    # Convert Django QuerySet objects into a list of dictionaries for JSON serialization
    filtered_data = []
    for order in orders:
        filtered_data.append({
            'pk': order.pk,
            'full_name': order.full_name,
            'phone_number': order.phone_number,
            'wilaya_display': order.wilaya_display, # Assuming this property exists on your Order model
            'wilaya_code': order.wilaya_display, # Useful if needed for frontend logic
            'commune': order.commune,
            "product": {
                'name': order.product.name, # Include product name for display
            },
            'product_id': order.product.pk, # Include product ID for potential frontend use (e.g., product links)
            'status': order.status,
            'status_display': order.get_status_display(), # Get human-readable status
            'quantity': order.quantity,
            'total_price': str(order.total_price), # Convert Decimal to string to avoid JSON serialization issues
            'is_confirmed': order.is_confirmed,
            'created_at': order.created_at.isoformat(), # Convert datetime to ISO string for JavaScript
            # Add any other fields you need in the frontend table
        })

    # Return the filtered data as a JSON response
    return render(request, 'orders/list.html', {
        'orders': filtered_data
    })  