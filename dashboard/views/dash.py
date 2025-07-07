from django.shortcuts import render
from django.contrib.auth import get_user_model
from dashboard.decorators import admin_required, role_required
from user_auth.models import UserProfile
from dashboard.models import Product, WaitList

userModel = get_user_model()

@role_required(["admin", "seller"])
def home(request):
    """
    Render the home page of the dashboard.
    """
    context = {}
    if request.user.profile.role == "admin":
        context['sellers'] = userModel.objects.filter(profile__role="seller")
        context['products'] = Product.objects.all()            
        context['waitlist'] = WaitList.objects.all() 
        context['orders'] = 0
    elif request.user.profile.role == "seller":
        context['products'] = Product.objects.filter(user=request.user)
        context['orders'] = 0  
    return render(request, 'dashboard/home.html', context=context) 