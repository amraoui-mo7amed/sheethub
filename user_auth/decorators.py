from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from functools import wraps
from django.urls import reverse

def redirect_user(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
            
        # Check if user has a profile
        if not hasattr(request.user, 'profile'):
            # Create a default profile if it doesn't exist
            from user_auth.models import UserProfile
            UserProfile.objects.create(user=request.user, role='seller')
            return redirect('dash:user_profile', pk=request.user.pk)
            
        # Redirect based on role
        if request.user.profile.role == 'admin':
            return redirect('dash:home')
            
        return redirect('dash:user_profile', pk=request.user.pk)
    return wrapper