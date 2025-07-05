import secrets
from django.utils import timezone
from django.urls import reverse
from user_auth.models import UserAuth

def generate_confirmation_link(request, user):
    """
    Generates a unique token, saves it to the user model, and returns the confirmation link.
    """
    token = secrets.token_urlsafe(32)  # Secure random token
    auth = UserAuth.objects.create(user=user)
    # Update user model
    auth.email_confirmation_token = token
    auth.email_confirmation_sent = timezone.now()
    auth.save()

    # Build full absolute confirmation URL
    relative_url = reverse('user_auth:confirm_email', kwargs={'token': token})
    activation_link = request.build_absolute_uri(relative_url)

    return activation_link


def generate_password_reset_link(request, user):
    """
    Generates a unique password reset token, saves it to the user model, and returns the password reset link.
    """
    token = secrets.token_urlsafe(32)  # Secure random token
    auth, created = UserAuth.objects.get_or_create(user=user)
    # Update user auth model with reset token and timestamp
    auth.password_reset_token = token
    auth.password_reset_sent = timezone.now()
    auth.save()

    # Build full absolute password reset URL
    relative_url = reverse('user_auth:reset_password_confirm', kwargs={'token': token})
    reset_link = request.build_absolute_uri(relative_url)

    return reset_link