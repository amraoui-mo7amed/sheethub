from .generic import *
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
