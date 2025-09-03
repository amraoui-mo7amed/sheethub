from django.shortcuts import render
from django.contrib.auth import get_user_model
from dashboard.decorators import admin_required, role_required
from dashboard.models import Product, WaitList
from subscription.models import UserSubscription
from frontend.models import Order
from django.utils import timezone
from django.db.models import F, FloatField, Sum, ExpressionWrapper, Count
from datetime import timedelta
from django.http import JsonResponse
from django.utils.translation import get_language, gettext_lazy as _
from django.db.models.functions import TruncDate


userModel = get_user_model()


@role_required(["admin", "seller"])
def home(request):
    """
    Render the home page of the dashboard.
    """

    context = {}
    if request.user.profile.role == "admin":
        context['sellers_count'] = userModel.objects.filter(profile__role="seller").count()
        context['top_sellers'] = (
            userModel.objects
            .filter(profile__role="seller")
            .annotate(order_count=Count('products__orders', distinct=True))
            .order_by('-order_count')[:6]
        )

        context['products'] = Product.objects.all()            
        context['waitlist'] = WaitList.objects.all() 
        context['orders'] = 0
    elif request.user.profile.role == "seller":
        context['products'] = Product.objects.filter(user=request.user)
        context['subPlan'] = UserSubscription.objects.get(user=request.user)
        context['orders'] = Order.objects.filter(product__user=request.user)
        context['delivered_revenue'] = float(
            Order.objects.filter(product__user=request.user, status="delivered")
            .aggregate(total=Sum(F("quantity") * F("product__price"), output_field=FloatField()))["total"] or 0
        )
    return render(request, 'dashboard/home.html', context=context) 



@role_required(["seller"])
def seller_data(request):
    """
    Return revenue, order count, and top products data for the seller,
    including stats for all statuses.
    Also returns revenue for shipped, confirmed, and cancelled orders for charting.
    """
    today = timezone.now().date()
    dates = [today - timedelta(days=i) for i in range(6, -1, -1)]
    labels = [d.strftime("%A") for d in dates]

    from frontend.models import Order
    status_choices = [s[0] for s in Order.STATUS_CHOICES]

    # Prepare stats per status
    status_stats = {}
    for status in status_choices:
        status_stats[status] = {
            "total_orders": Order.objects.filter(
                product__user=request.user,
                status=status
            ).count(),
            "total_revenue": float(
                Order.objects.filter(
                    product__user=request.user,
                    status=status
                ).aggregate(
                    total=Sum(F("quantity") * F("product__price"), output_field=FloatField())
                )["total"] or 0
            )
        }

    # Revenue per day for each status
    status_revenue_per_day = {
        "confirmed": [],
        "shipped": [],
        "cancelled": []
    }
    for day in dates:
        for status in status_revenue_per_day.keys():
            orders_qs = Order.objects.filter(
                product__user=request.user,
                created_at__date=day,
                status=status
            ).annotate(
                total_price=ExpressionWrapper(
                    F("quantity") * F("product__price"),
                    output_field=FloatField()
                )
            )
            total = orders_qs.aggregate(total=Sum("total_price"))["total"] or 0
            status_revenue_per_day[status].append(float(total))

    # Revenue and order count per day (all statuses)
    revenue_amounts = []
    order_counts = []
    for day in dates:
        orders_qs = Order.objects.filter(
            product__user=request.user,
            created_at__date=day
        ).annotate(
            total_price=ExpressionWrapper(
                F("quantity") * F("product__price"),
                output_field=FloatField()
            )
        )
        total = orders_qs.aggregate(total=Sum("total_price"))["total"] or 0
        count = orders_qs.aggregate(count=Count("id"))["count"] or 0
        revenue_amounts.append(float(total))
        order_counts.append(count)

    # Total revenue from all orders (all statuses)
    total_revenue = float(
        Order.objects.filter(product__user=request.user)
        .aggregate(total=Sum(F("quantity") * F("product__price"), output_field=FloatField()))["total"] or 0
    )

    # Top 5 products by sales quantity (all statuses)
    top_products = (
        Order.objects.filter(product__user=request.user)
        .values("product__name")
        .annotate(total_quantity=Sum("quantity"))
        .order_by("-total_quantity")[:5]
    )
    top_products_labels = [item["product__name"] for item in top_products]
    top_products_values = [item["total_quantity"] for item in top_products]

    return JsonResponse({
        "labels": labels,
        "revenue": revenue_amounts,
        "orders": order_counts,
        "total_revenue": total_revenue,
        "status_stats": status_stats,
        "top_products_labels": top_products_labels,
        "top_products_values": top_products_values,
        "status_revenue_per_day": status_revenue_per_day,  # <-- for charting
    })


@role_required(['admin'])
def admin_data(request):
    end_date   = timezone.now().date()
    start_date = end_date - timedelta(days=6)
    labels     = [str(start_date + timedelta(days=i)) for i in range(7)]

    # new sellers
    sellers_qs = (
        userModel.objects
        .filter(profile__role='seller', date_joined__date__gte=start_date)
        .annotate(day=TruncDate('date_joined'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    sellers_map = {str(item['day']): item['count'] for item in sellers_qs}
    sellers_per_day = [sellers_map.get(l, 0) for l in labels]

    # deliveries (orders)
    orders_qs = (
        Order.objects
        .filter(created_at__date__gte=start_date)
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    orders_map = {str(item['day']): item['count'] for item in orders_qs}
    deliveries_per_day = [orders_map.get(l, 0) for l in labels]

    # top 5 products by revenue
    top_products = (
        Product.objects
        .filter(orders__created_at__date__gte=start_date)
        .annotate(revenue=Sum(F('orders__quantity') * F('price')))
        .order_by('-revenue')[:5]
    )

    return JsonResponse({
        'labels': labels,
        'sellers_per_day': sellers_per_day,
        'deliveries_per_day': deliveries_per_day,
        'orders_per_day': deliveries_per_day,
        'top_products_labels': [p.name for p in top_products],
        'top_products_values': [float(p.revenue or 0) for p in top_products],

        # phrases
        'phrases': {
            'new_sellers': str(_('New Sellers')),
            'deliveries' : str(_('Deliveries')),
            'orders'     : str(_('Orders')),
            'top_products': str(_('Top Products')),
        }
    })