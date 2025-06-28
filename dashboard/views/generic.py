from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _

@login_required
def BaseDelete(request, Model, pk, user_field=None):
    try:
        # Get the model class dynamically
        model = Model
        instance = model.objects.get(pk=pk)
        
        # Check ownership if user_field is specified
        if user_field and hasattr(instance, user_field):
            owner = getattr(instance, user_field)
            if owner != request.user:
                return JsonResponse({
                    'status': 'error', 
                    'message': _('You do not have permission to delete this item')
                }, status=403)
        
        instance.delete()
        return JsonResponse({
            'status': 'success', 
            'message': _('Item deleted successfully')
        })
    except model.DoesNotExist:
        return JsonResponse({
            'status': 'error', 
            'message': _('Item not found')
        }, status=404)
    except LookupError:
        return JsonResponse({
            'status': 'error', 
            'message': _('Invalid model')
        }, status=400)
    
    
class BaseListView(LoginRequiredMixin, ListView):
    model = None  # This will be set dynamically
    template_name = 'dashboard/base_list.html'  # You can customize this template

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objects'] = context['object_list']  # Add the objects as 'objects' key
        return context