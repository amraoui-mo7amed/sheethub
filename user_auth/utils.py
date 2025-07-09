import secrets
from django.utils import timezone
from django.urls import reverse
from user_auth.models import UserAuth
from mailjet import MailJet
from django.http import JsonResponse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import logout

def generate_confirmation_link(request, user):
    """
    Generates a unique token, saves it to the user model, and returns the confirmation link.
    """
    token = secrets.token_urlsafe(32)  # Secure random token
    auth,created = UserAuth.objects.get_or_create(user=user)
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


def sendActivationeEmail(request):
    try:
        if request.user.is_authenticated:
            logout(request)
        user = request.user
        first_name = user.first_name or "User"
        email = user.email

        activation_link = generate_confirmation_link(request, user)
        mailjet = MailJet()
        success, response = mailjet.sendMessage(
            templateID=mailjet.account_activation_templateID,
            subject=str(_("Sheethub Account activation")),
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
            return JsonResponse({"success": True, "message": _("Activation email sent successfully!")})
        else:
            return JsonResponse({"success": False, "message": _("Failed to send activation email.")})

    except Exception as e:
        return JsonResponse({"success": False, "message": _("Something went wrong. Please try again {e}.").format(e=e)})
