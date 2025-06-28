from django.shortcuts import render, redirect
from functools import wraps
from django.core.exceptions import PermissionDenied


def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('user_auth:login')  # Redirect to your custom dashboard
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def role_required(allowed_roles=None):
    """
    Decorator to check if user has required role(s)

    Args:
        allowed_roles (str|list): Single role or list of allowed roles
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('user_auth:login')

            # Convert single role to list
            roles = [allowed_roles] if isinstance(allowed_roles, str) else allowed_roles

            # Check if user's role is in allowed roles
            if not roles or request.user.profile.role not in roles:
                raise PermissionDenied("You don't have permission to access this page")

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


