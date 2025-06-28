from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse_lazy
from .models import SubscriptionPlan
from dashboard.views.generic import BaseListView, BaseDelete
from dashboard.mixins import AdminRequiredMixin
from dashboard.decorators import admin_required
from django.contrib.auth.decorators import login_required
from .models import SubscriptionPlan
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

# Create your views here.

class PlanListView(AdminRequiredMixin, BaseListView):
    model = SubscriptionPlan
    template_name = 'subscription/list.html'
    context_object_name = 'plans'
    

@login_required
@admin_required
def create(request):
    if request.user.is_staff:
        if request.method == 'POST':
            errors = []
            
            # Validate required fields
            name = request.POST.get('name', '').strip()
            if not name:
                errors.append(_("Plan name is required"))
            elif len(name) > 20:
                errors.append(_("Name must be 20 characters or less"))
                
            try:
                price = float(request.POST.get('price', 0))
            except ValueError:
                errors.append(_("Invalid price format"))
                
            try:
                max_orders = int(request.POST.get('max_orders', 0))
                if max_orders <= 0:
                    errors.append(_("Max orders must be at least 1"))
            except ValueError:
                errors.append(_("Invalid max orders value"))
                
            try:
                max_products = int(request.POST.get('max_products', 0))
                if max_products <= 0:
                    errors.append(_("Max products must be at least 1"))
            except ValueError:
                errors.append(_("Invalid max products value"))
            
            if errors:
                return JsonResponse({'success': False, 'errors': errors}, status=400)
                
            # Create the plan if no errors
            plan = SubscriptionPlan.objects.create(
                name=name,
                price=price,
                max_orders=max_orders,
                max_products=max_products,
                can_export='can_export' in request.POST,
                email_support='email_support' in request.POST,
                can_import='can_import' in request.POST,
                has_analytics='has_analytics' in request.POST
            )
            
            return JsonResponse({'success': True, 'redirect_url' : reverse_lazy('subs:plans')})
            
        return JsonResponse({'success': False, 'errors': [_('Invalid request method')]}, status=405)
    
    return JsonResponse({'success': False, 'errors': [_('Permission denied')]}, status=403)



@admin_required
def Delete(request, pk):
    return BaseDelete(request, SubscriptionPlan, pk)