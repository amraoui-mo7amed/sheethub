from django.shortcuts import render
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from dashboard.models import WaitList


def index(request):
    """
    Render the index page.
    """
    return render(request, 'frontend/index.html')

def waitlist(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        errors = []

        if not name or not email :
            errors.append(_("Name and email are required"))
        if not email :
            errors.append(_("Email is required"))
        if not name :
            errors.append(_("Name is required"))
        
        if "@" not in email:
            errors.append(_("Invalid email"))

        if not errors:
            try: 
                WaitList.objects.create(
                    fullname = name,
                    email = email
                )
                return JsonResponse({
                    "success" : True, 
                    "message" : _("Thank you for joining our waitlist")
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

def terms(request):
    """
    Render the terms and conditions page.
    """
    return render(request, 'frontend/terms.html')


from django.http import HttpResponse

def domain_verification(request):
    return HttpResponse("", content_type="text/plain")  # empty content
