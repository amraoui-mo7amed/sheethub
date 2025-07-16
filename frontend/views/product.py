from .generic import *

def product_landing(request,shop_code,pk):
    product = get_object_or_404(Product, pk=pk, is_public=True)
    landing = getattr(product, 'landing_page', None)
    algeria = loadJSON('algeria.json')

    if landing.landing_language == 'en' or landing.landing_language == 'fr':
        unique_wilayas = {(entry["wilaya_code"], entry["wilaya_name_ascii"]) for entry in algeria}
    else:
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