from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from functools import wraps
from django.urls import reverse

def redirect_user(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Get user role from profile
            role = request.user.profile.role
            
            # Redirect based on role
            if role == 'admin':
                return redirect('dash:home')
            else: 
                return redirect(reverse('dashboard:user_profile', kwargs={'pk': request.user.pk}))
 
        return view_func(request, *args, **kwargs)
    return wrapper