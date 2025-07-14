from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.db import transaction
import geolocation as gl
from user_auth.models import UserAuth, UserProfile
from user_auth.decorators import redirect_user
from user_auth.utils import generate_confirmation_link
from mailjet import MailJet

userModel = get_user_model()

@csrf_exempt
@redirect_user
def signup(request):
    if request.method == 'POST':
        errors = []
        
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        # Get the geoLocations 
        try:
            ip = gl.get_client_ip(request)
            geolocation = gl.get_geolocation(ip)
            country = geolocation.get('country')
        except Exception as e:
            country = None
        
        print(country)
        # Validate names
        if not first_name or not last_name:
            errors.append(_('First and last name are required'))
        elif len(first_name) < 2 or len(last_name) < 2:
            errors.append(_('Names must be at least 2 characters long'))

        # Validate email
        try:
            validate_email(email)
            if userModel.objects.filter(email=email).exists():
                errors.append(_('This email is already registered'))
        except ValidationError:
            errors.append(_('Please enter a valid email address'))

        # Validate password
        if not password1:
            errors.append(_('Password is required'))
        elif len(password1) < 8:
            errors.append(_('Password must be at least 8 characters long'))
        elif password1 != password2:
            errors.append(_('Passwords do not match'))

        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)

        try:
            # Set default values
            is_beta = False
            max_orders = 30
            max_products = 1
            
            # Override for first 10 users
            if userModel.objects.all().count() <= 10:
                is_beta = True
                max_orders = 150
                max_products = 5
            with transaction.atomic():
                user = userModel.objects.create_user(
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name,
                )
                profile = UserProfile.objects.create(
                    user=user, 
                    role='seller', 
                    max_orders = max_orders, 
                    max_products = max_products,
                    is_beta = is_beta, 
                    country=country)
                user.profile = profile
                user.save()

                activation_link = generate_confirmation_link(request, user)
                mailjet = MailJet()
                success, response = mailjet.sendMessage(
                    templateID=mailjet.account_activation_templateID,
                    subject=str(_("Sheethub Account activation")),
                    type="noreply",
                    variabels={
                        "activation_link": activation_link,
                        "first_name": first_name,
                        "greetings": str(_("Hello")),
                        "title": str(_("Welcome to Sheethub!")),
                        "subject": str(_("Please confirm your email address")),
                        "sender": str(_("Sheethub Team")),
                        "warning": str(_("If you didn't create an account, please ignore this email.")),
                        "confirm_button_text": str(_("Activate Account")),
                        "text": str(_("Thank you for signing up! Please click the button below to activate your account:")),
                    },
                    recipiant_email=email,
                    recipiant_name=first_name
                )

                if success:
                    return JsonResponse({
                        'success': True,
                        'message': _('E-mail activation link has been sent successfully. Please activate your account.'),
                    })

                errors.append(_('E-mail activation link could not be sent. Please try again.'))
        except Exception as e:
            errors.append(str(e))

        return JsonResponse({'success': False, 'errors': errors}, status=400)

    return render(request, 'user_auth/signup.html', {
        'today': timezone.now().date()
    })


@csrf_exempt
@redirect_user
def signin(request):
    if request.method == 'POST':
        errors = []
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        try:
            validate_email(email)
        except ValidationError:
            errors.append(_('Please enter a valid email address'))

        if not email or not password:
            errors.append(_('All fields are required'))
        elif len(password) < 4:
            errors.append(_('Password must be at least 4 characters long'))

        if not errors:
            try:
                user = authenticate(request, email=email, password=password)
                if user:
                    if user.is_active:
                        login(request, user)
                        redirect_url = reverse_lazy('dash:user_profile', kwargs={'pk': user.pk}) \
                            if user.profile.role in ['organizer', 'participant'] else reverse_lazy('dash:home')
                        return JsonResponse({'success': True, 'redirect_url': redirect_url})
                    else:
                        errors.append(_('Your account is not active. Please check your email for the activation link.'))
                else:
                    errors.append(_('Invalid email address or password.'))
            except Exception as e:
                errors.append(str(e))

        return JsonResponse({'success': False, 'errors': errors}, status=400)

    if request.user.is_authenticated:
        return redirect(reverse_lazy('dash:home'))

    return render(request, 'user_auth/login.html')


def signout(request):
    logout(request)
    return redirect('user_auth:login')
