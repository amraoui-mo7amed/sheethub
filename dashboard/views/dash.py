from django.shortcuts import render
from django.contrib.auth import get_user_model
from dashboard.decorators import admin_required
from user_auth.models import UserProfile

userModel = get_user_model()

@admin_required
def home(request):
    """
    Render the home page of the dashboard.
    """
    context = {
        'users': userModel.objects.all().select_related('profile')
            .order_by('-date_joined')
            .exclude(is_superuser=True),
    }
    return render(request, 'dashboard/home.html', context=context) 