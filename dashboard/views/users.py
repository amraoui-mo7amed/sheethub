from django.urls import reverse_lazy, reverse
from .generic import *
from dashboard.mixins import AdminRequiredMixin
from dashboard.decorators import admin_required
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from dashboard.decorators import role_required, admin_required, user_is_self
from utils import loadJSON
from dashboard.utils import create_user_notification

userModel = get_user_model()

class list( AdminRequiredMixin ,BaseListView):
    model = userModel 
    template_name = "users/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objects'] = userModel.objects.all().exclude(is_staff=True)
        return context

@login_required
@admin_required
def Delete(request, pk):
    return BaseDelete(request,userModel,pk)

@login_required
@user_is_self
def userProfile(request, pk):
    user = get_object_or_404(userModel, pk=pk)
    context = {
        'user' : user
    }
    return render(request, 'users/profile.html', context = context)

@login_required
def profileEdit(request):
    user = request.user
    print(user)
    if request.method == 'POST':
        image = request.FILES.get('image')  # Changed to request.FILES for file upload
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        errors = []

        if not first_name:  # Simplified validation
            errors.append(_("First name is required"))
        if not last_name:  # Simplified validation
            errors.append(_("Last name is required"))
        
        if errors:
            print(errors)
            return JsonResponse({
                'success': False,
                'errors': errors
            }, status=400)
            
        try:
            # Update user fields
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            # Handle image upload if provided
            if image:
                user.profile.image = image
                user.profile.save()
            return JsonResponse({
                'success': True,
                'redirect_url': reverse('dash:home')  # Changed to reverse
            })
            
        except Exception as e:
            print(e)
            return JsonResponse({
                'success': False,
                'errors': [str(e)]
            }, status=500)
    
    # Handle GET request
    print("invalid")
    return JsonResponse({
        'success': False,
        'errors': ['Invalid request method']
    }, status=405)