from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import send_mail
from django.conf import settings
from user_auth.models import UserAuth
import uuid
from datetime import timedelta, datetime
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from user_auth.utils import generate_password_reset_link
from mailjet import MailJet
from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from user_auth.decorators import redirect_user

userModel = get_user_model()

@redirect_user
def forgot_password(request):

    if request.method == "POST":
        errors = []
        email = request.POST.get('email')

        if not email:
            errors.append(_('Email is required.'))

        try:
            validate_email(email)
        except ValidationError:
            errors.append(_('Invalid email address.'))
        
        try:
            user = userModel.objects.get(email=email)
        except userModel.DoesNotExist:
            errors.append(_("E-mail address not found"))
        
        if not errors:
            try:
                mailjet = MailJet()
                reset_link = generate_password_reset_link(request, user)
                
                success, response = mailjet.sendMessage(
                    templateID=7132960,
                    subject=str(_("Password Reset Request")),
                    variabels= {
                        "template_text": str(_("You requested a password reset. Please click the link below to set a new password.")),
                        "activation_link": reset_link,
                        "rest_text": str(_("Reset Password")),
                        "template_title": str(_("Password Reset Request"))
                        },
                    recipiant_email=email,
                    recipiant_name=user.first_name
                )
                
                if success:
                    return JsonResponse({'success': True, 'message': _('Password reset email sent successfully.')})
                else:
                    return JsonResponse({'success': False, 'errors': [str(response)]}, status=400)
            except Exception as e:
                return JsonResponse({'success': False, 'errors': [str(e)]}, status=400)
        else:
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        return render(request, 'user_auth/forgot_password.html')

@redirect_user
def password_reset_confirm(request, token):
    """
    Confirm password reset using a secure token.
    """
    context = {
        'valid_link': False,
        'token': token,
        "error_messages" : []
    }

    try:
        user_auth = UserAuth.objects.get(password_reset_token=token)
        if user_auth.password_reset_token is None or user_auth.password_reset_token != token:
            context['error_messages'].append(_("Invalid or expired password reset link."))
        else:
            # Check expiration (24 hours)
            if timezone.now() > user_auth.password_reset_sent + timedelta(hours=24):
                context['valid_link'] = False
            else:
                # Valid link
                context['valid_link'] = True
        
        if request.method == 'POST':
            errors = []
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            # Basic validation
            if not password or not confirm_password:
                errors.append(_('Please fill in all fields.'))
            elif password != confirm_password:
                errors.append(_("Passwords don't match."))
            elif len(password) < 8:
                errors.append(_("Password must be at least 8 characters long."))
            
            if not errors:
                user = user_auth.user
                user.set_password(password)
                user.save()

                # Invalidate token
                user_auth.password_reset_token = None
                user_auth.save()

                return JsonResponse({'success': True, "redirect_url" : reverse_lazy('user_auth:login')})
            if errors : 
                return JsonResponse({'success': False, 'errors': errors})

    except UserAuth.DoesNotExist:
        context['error_messages'].append(_("Invalid or expired password reset link."))

    return render(request, 'user_auth/reset_password_confirm.html', context)
