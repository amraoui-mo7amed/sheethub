from .generic import *
from frontend.models import Contact
from django.utils.translation import gettext_lazy as _

def create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        errors = []
        if not name or not email or not subject or not message:
            errors.append(_("All fields are required"))

        if "@" not in email:
            errors.append(_("Invalid email"))

        if not errors:
            try:
                Contact.objects.create(
                    name = name,
                    email = email,
                    subject = subject,
                    message = message
                )
                return JsonResponse({
                    "success" : True, 
                    "message" : _("Message Has Been Sent Succefully, we'll reply as soon as possible")
                })
            except Exception as e:
                errors.append(str(e))
                return JsonResponse({
                    "success" : False, 
                    "errors" : errors
                })
    else:
        return JsonResponse({
            "success" : False, 
            "errors" : [_("Invalid request method")]
        })