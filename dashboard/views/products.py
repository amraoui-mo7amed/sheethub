from django.urls import reverse_lazy, reverse
from .generic import *
from dashboard.mixins import AdminRequiredMixin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from dashboard.decorators import role_required, admin_required, user_is_self
from dashboard.models import Product, ProductImage, LandingPageConfig
from django.http import JsonResponse
from .generic import BaseDelete
from utils import loadJSON

userModel = get_user_model()

@login_required
@role_required(["seller"])
def list(request): 
    Products = Product.objects.filter(user=request.user)
    return render(request, "products/list.html", {"products": Products})


@login_required
@role_required(["seller"])
def create(request):
    if request.method == "POST":
        errors = []

        # Extract data
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        price = request.POST.get("price", "").strip()
        stock = request.POST.get("stock", "").strip()
        is_public = bool(request.POST.get("is_public"))
        is_featured = bool(request.POST.get("is_featured"))
        in_stock = bool(request.POST.get("in_stock", True))
        allow_additional_images = bool(request.POST.get("allow_additional_images"))
        enable_pixel = bool(request.POST.get("enable_pixel"))
        facebook_pixel_id = request.POST.get("facebook_pixel_id", "").strip()
        landing_language = request.POST.get("landing_language", "").strip()
        layout_direction = request.POST.get("layout_direction", "").strip()
        enable_feedbacks = bool(request.POST.get("enable_feedbacks"))
        enable_related_products = bool(request.POST.get("enable_related_products"))
        image = request.FILES.get("default_image")

        # === Validation ===
        if not name:
            errors.append(_("Product name is required"))

        if not price:
            errors.append(_("Price is required"))
        else:
            try:
                price = float(price)
            except ValueError:
                errors.append(_("Price must be a valid number"))

        if not image:
            errors.append(_("Main product image is required"))

        try:
            stock = int(stock or 0)
        except ValueError:
            errors.append(_("Stock must be an integer"))

        if not description:
            errors.append(_("Product description is required"))

        if enable_pixel and not facebook_pixel_id:
            errors.append(_("Facebook Pixel ID is required when tracking is enabled"))

        if allow_additional_images:
            found = False
            for file_key in request.FILES:
                if "image" in file_key and file_key != "default_image":
                    found = True
                    break
            if not found:
                errors.append(_("At least one additional image is required"))

        if not landing_language:
            errors.append(_("Landing page language is required"))

        if not layout_direction:
            errors.append(_("Layout direction is required"))

        if errors:
            return JsonResponse({
                'success': False,
                'errors': errors
            })

        # === Save Product ===
        product = Product.objects.create(
            user=request.user,
            name=name,
            description=description,
            price=price,
            stock=stock,
            image=image,
            is_public=is_public,
            is_featured=is_featured,
            in_stock=in_stock,
            allow_additional_images=allow_additional_images,
            enable_pixel=enable_pixel,
            facebook_pixel_id=facebook_pixel_id,
        )

        # === Save Landing Page Config ===
        LandingPageConfig.objects.create(
            product=product,
            landing_language=landing_language,
            layout_direction=layout_direction,
            enable_feedbacks=enable_feedbacks,
            enable_related_products=enable_related_products
        )

        # === Save Additional Images ===
        if allow_additional_images:
            for file_key in request.FILES:
                if "image" in file_key and file_key != "default_image":
                    ProductImage.objects.create(product=product, image=request.FILES[file_key])

        return JsonResponse({
            'success': True,
            'redirect_url': reverse_lazy('dash:products_list')
        })

    else:
        return render(request, "products/create.html")


@login_required
@role_required(["seller"])
def productDetails(request, pk): 
    product = get_object_or_404(Product, pk=pk, user=request.user)
    return render(request, "products/details.html", {"product": product})

@role_required(["seller"])
def Delete(request, pk):
    return BaseDelete(request,Product,pk)
