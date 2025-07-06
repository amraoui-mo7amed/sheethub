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
from datetime import timedelta
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from user_auth.models import UserAuth
from user_auth.decorators import redirect_user

userModel = get_user_model()


@redirect_user
def confirm_email_view(request, token):
    try:
        user_auth = get_object_or_404(UserAuth, email_confirmation_token=token)
        if timezone.now() > user_auth.email_confirmation_sent + timedelta(hours=24):
            return render(request, 'user_auth/email_confirmation.html', {
                'success': False,
                'message': _('The confirmation link has expired. Please request a new one.')
            })
        
        user_auth.email_confirmed = True
        user_auth.email_confirmation_token = None
        user_auth.save()
        
        return render(request, 'user_auth/email_confirmation.html', {
            'success': True,
            'message': _('Your email has been successfully confirmed! You can now log in.')
        })
        
    except Exception as e:
        return render(request, 'user_auth/email_confirmation.html', {
            'success': False,
            'message': _('Invalid confirmation link. Please try again.')
        })