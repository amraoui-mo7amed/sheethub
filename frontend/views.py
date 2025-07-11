from django.shortcuts import render, get_object_or_404
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from dashboard.models import WaitList, Product
from subscription.models import SubscriptionPlan
from utils import loadJSON

def index(request):
    """
    Render the index page.
    """
    context= {
        'plans': SubscriptionPlan.objects.all()
    }
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


def product_landing(request,shop_code,pk):
    product = get_object_or_404(Product, pk=pk, is_public=True)
    landing = getattr(product, 'landing_page', None)
    algeria = loadJSON('algeria.json')
    unique_wilayas = {(entry["wilaya_code"], entry["wilaya_name"]) for entry in algeria}
    sorted_wilayas = sorted(list(unique_wilayas), key=lambda x: x[0])

    if not landing:
        # Optional fallback or 404
        return render(request, "products/landing_not_configured.html", {"product": product})

    context = {
        "product": product,
        "landing": landing,
        "wilayas": sorted_wilayas
    }

    return render(request, "products/landing_page.html", context)

def getCommunes(request, province_id):
    algeria = loadJSON('algeria.json')
    print(province_id)
    if province_id:
        communes = [entry for entry in algeria if entry['wilaya_code'] == f"{int(province_id):02}"]
    else:
        communes = []
    return JsonResponse(communes, safe=False)