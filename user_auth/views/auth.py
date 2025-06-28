from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import send_mail
from django.conf import settings
from user_auth.models import UserAuth, UserProfile
import uuid
from datetime import timedelta
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
import re
from django.db import transaction
from user_auth.decorators import redirect_user
from django.contrib.auth.decorators import login_required

userModel = get_user_model()

@csrf_exempt
@redirect_user
def signin(request):

    if request.method == 'POST':
        errors = []
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            errors.append(_('Please enter a valid email address'))
            
        # Validate required fields
        if not email or not password:
            errors.append(_('All fields are required'))
        
        # Validate password length
        if len(password) < 4:
            errors.append(_('Password must be at least 4 characters'))
            
        if not errors:
            try:
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        redirect_url = None
                        if user.profile.role == 'organizer' or user.profile.role == 'participant':
                            redirect_url = reverse_lazy('dash:user_profile', kwargs={'pk': user.pk})
                        else:
                            redirect_url = reverse_lazy('dash:home')
                        return JsonResponse({
                            'success': True,
                            'redirect_url': redirect_url
                        })
                    else:
                        errors.append(_('Your account is not active. Please check your email for activation link'))
                else:
                    errors.append(_('Invalid email address or password'))
            except Exception as e:
                errors.append(str(e))
        return JsonResponse({
            'success': False,
            'errors': errors
        }, status=400)
    
    if request.user.is_authenticated:
        return redirect(reverse_lazy('dash:home'))
    return render(request, 'user_auth/login.html')

@csrf_exempt
@redirect_user
def signup(request):
    if request.method == 'POST':
        errors = []
        
        # Get form data
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        mobile = request.POST.get('mobile', '').strip()
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        city = request.POST.get('city')
        role = request.POST.get('role')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        terms = request.POST.get('terms')
        
        # Validate name fields
        if not first_name or not last_name:
            errors.append( _('First and last name are required'))
        elif len(first_name) < 2 or len(last_name) < 2:
            errors.append(_('Names must be at least 2 characters long'))
        
        # Validate email
        try:
            validate_email(email)
            if userModel.objects.filter(email=email).exists():
                errors.append(_('This email is already registered'))
        except ValidationError:
            errors.append( _('Please enter a valid email address'))
        
        # Validate mobile
        if len(mobile) != 9:  # Changed from 8 to 9
            errors.append(_('Mobile number must be 9 digits long'))  # Updated message
        if not re.match(r'^[5-7][0-9]{8}$', mobile):
            errors.append(_('Please enter a valid mobile number'))
        elif UserProfile.objects.filter(mobile=mobile).exists():
            errors.append(_('This mobile number is already registered'))

        # Validate gender
        if gender not in ['M', 'F']:
            errors.append (_('Please select your gender'))
            
        # Validate date of birth
        try:
            dob = timezone.datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            age = (timezone.now().date() - dob).days / 365.25
            if age < 13:
                errors.append( _('You must be at least 13 years old'))
            elif age > 100:
                errors.append( _('Invalid date of birth'))
        except (ValueError, TypeError):
            errors.append(_('Please enter a valid date of birth'))
            
        # Validate city
        try:
            city_id = int(city)
            if not 1 <= city_id <= 58:
                errors.append( _('Please select a valid province'))
        except (ValueError, TypeError):
            errors.append( _('Please select your province'))
            
        # Validate role
        if role not in ['participant', 'organizer']:
            errors.append( _('Please select a valid role'))
            
        # Validate password
        if not password1:
            errors.append( _('Password is required'))
        elif len(password1) < 4:
            errors.append( _('Password must be at least 8 characters long'))
        # elif not re.search(r'[A-Z]', password1):
        #     errors.append( _('Password must contain at least one uppercase letter'))
        # elif not re.search(r'[a-z]', password1):
        #     errors.append({'field': 'password1', 'message': _('Password must contain at least one lowercase letter')})
        # elif not re.search(r'[0-9]', password1):
        #     errors.append({'field': 'password1', 'message': _('Password must contain at least one number')})
            
        # Validate password confirmation
        if password1 != password2:
            errors.append( _('Passwords do not match'))
            
        # Validate terms acceptance
        if not terms:
            errors.append(_('You must accept the terms and conditions'))
            
        # Only create user if there are no errors
        if not errors:
            try:
                # Start transaction to ensure both user and profile are created or neither
                    # Create user first
                    user = userModel.objects.create_user(
                        email=email,
                        password=password1,
                        first_name=first_name,
                        last_name=last_name,
                    )
                    
                    # Create profile and properly link it to user
                    profile = UserProfile.objects.create(
                        user=user,  # This fixes the NOT NULL constraint
                        mobile=mobile,
                        gender=gender,
                        date_of_birth=date_of_birth,
                        city=city,
                        role=role,
                        nationality='DZ'
                    )
                    user.profile = profile
                    user.save()
                    # Log user in
                    login(request, user)
                    
                    return JsonResponse({
                        'success': True,
                        'message': _('Account created successfully'),
                        'redirect_url': reverse('dash:home')
                    })
                    
            except Exception as e:
                # Add the error and return error response
                errors.append(str(e))
        
        # Return all errors if any
        return JsonResponse({
            'success': False,
            'errors': errors
        }, status=400)

    # For GET requests, render the signup form
    context = {
        'today': timezone.now().date()
    }
    return render(request, 'user_auth/signup.html', context)

def signout(request):
    logout(request)
    return redirect('user_auth:login')
