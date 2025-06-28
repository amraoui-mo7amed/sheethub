from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin
from django.utils.translation import gettext_lazy as _

class AdminRequiredMixin(AccessMixin):
    """Verify that the current user is staff."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class RoleRequiredMixin(AccessMixin):
    """Verify that the current user has one of the required roles."""
    required_roles = None  # Can be a single role string or a list of roles

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if not hasattr(request.user, 'role'):
            return self.handle_no_permission()
        
        # Convert single role to list if needed
        roles = self.get_required_roles()
        if isinstance(roles, str):
            roles = [roles]
            
        if request.user.role not in roles:
            return self.handle_no_permission()
        
        return super().dispatch(request, *args, **kwargs)

    def get_required_roles(self):
        """Return the required roles."""
        return self.required_roles

    def get_permission_denied_message(self):
        """Return the message to show when the user doesn't have the required role."""
        roles = self.get_required_roles()
        if isinstance(roles, str):
            return _('You do not have the required role to access this page.')
        return _('You do not have any of the required roles to access this page.')

