from .generic import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from dashboard.models import Product
from frontend.models import Order

def getCommunes(request, province_id, lang_code):
    algeria = loadJSON('algeria.json')
    filtered = [entry for entry in algeria if entry['wilaya_code'] == f"{int(province_id):02}"]

    # Select field names depending on the lang
    if lang_code.lower() == 'ar':
        communes = [
            {
                "id": entry["id"],
                "commune_name": entry["commune_name"],
                "wilaya_name": entry["wilaya_name"]
            }
            for entry in filtered
        ]
    else:  # 'fr', 'en', or default
        communes = [
            {
                "id": entry["id"],
                "commune_name": entry["commune_name_ascii"],
                "wilaya_name": entry["wilaya_name_ascii"]
            }
            for entry in filtered
        ]

    return JsonResponse(communes, safe=False)


@csrf_exempt
def submit_order(request, product_id):
    if request.method != "POST":
        return JsonResponse({"success": False, "errors": ["Invalid request method."]})

    errors = []

    try:
        product = Product.objects.get(id=product_id)
        lang = product.landing_page.landing_language
    except Product.DoesNotExist:
        return JsonResponse({"success": False, "errors": ["Product not found."]})
    except Exception:
        return JsonResponse({"success": False, "errors": ["Landing page config missing."]})

    def t(ar, fr, en):
        return ar if lang == 'ar' else fr if lang == 'fr' else en

    # Extract form fields
    fullname = request.POST.get("fullname", "").strip()
    email = request.POST.get("email", "").strip()
    phone = request.POST.get("phone", "").strip()
    wilaya = request.POST.get("wilaya", "").strip()
    commune = request.POST.get("commune", "").strip()
    quantity = request.POST.get("quantity", "").strip()

    # Validation
    if not fullname:
        errors.append(t("الاسم الكامل مطلوب", "Le nom complet est requis", "Full name is required"))

    if not email:
        errors.append(t("البريد الإلكتروني مطلوب", "L'email est requis", "Email is required"))

    if not phone or not phone.isdigit() or not phone.startswith(('5', '6', '7')) or len(phone) != 9:
        errors.append(t("رقم الهاتف غير صالح", "Numéro de téléphone invalide", "Invalid phone number"))

    if not wilaya:
        errors.append(t("الولاية مطلوبة", "La wilaya est requise", "Province is required"))

    if not commune:
        errors.append(t("البلدية مطلوبة", "La commune est requise", "Commune is required"))

    try:
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError()
    except:
        errors.append(t("الكمية غير صالحة", "Quantité invalide", "Invalid quantity"))

    # Handle errors
    if errors:
        return JsonResponse({"success": False, "errors": errors})

    # Save Order
    order = Order.objects.create(
        product=product,
        full_name=fullname,
        email=email,
        phone_number=phone,
        wilaya=wilaya,
        commune=commune,
        quantity=quantity,
        created_at=now()
    )
    product.stock -= quantity
    product.save()
    return JsonResponse({
        "success": True,
        "message": t("تم إرسال الطلب بنجاح", "Commande envoyée avec succès", "Order submitted successfully"),
    })
