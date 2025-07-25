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
from django.http import JsonResponse
from django.core.serializers import serialize
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from subscription.models import UserSubscription
from django.core.exceptions import ValidationError
from django.db import transaction

userModel = get_user_model()

@login_required
@role_required(["admin","seller"])
def list(request): 
    if request.user.profile.role == "admin":
        Products = Product.objects.all()
    else:
        Products = Product.objects.filter(user=request.user)
    return render(request, "products/list.html", {"products": Products})

@login_required
@role_required(["seller"])
def create_or_update_product(request, pk=None):
    if request.method == "POST":
        is_update = pk is not None
        userPlan = UserSubscription.objects.get(user=request.user)
        errors = []

        product = None
        if is_update:
            product = get_object_or_404(Product, pk=pk, user=request.user)

        # Extract form data
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        price = request.POST.get("price", "").strip()
        stock = request.POST.get("stock", "").strip()
        is_public = True
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

        if not is_update and not image:
            errors.append(_("Main product image is required"))

        try:
            stock = int(stock or 0)
        except ValueError:
            errors.append(_("Stock must be an integer"))

        if not description:
            errors.append(_("Product description is required"))

        if enable_pixel and not facebook_pixel_id:
            errors.append(_("Facebook Pixel ID is required when tracking is enabled"))

        if not landing_language:
            errors.append(_("Landing page language is required"))

        if not layout_direction:
            errors.append(_("Layout direction is required"))

        if not is_update and userPlan.plan.max_products <= 0:
            errors.append(_("You have reached the maximum number of products allowed"))

        if allow_additional_images and not is_update:
            found = any(k.startswith("image_") for k in request.FILES)
            if not found:
                errors.append(_("At least one additional image is required"))

        if errors:
            return JsonResponse({'success': False, 'errors': errors})

        # === Save or Update ===
        if not is_update:
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
            userPlan.plan.save()
            userPlan.save()
        else:
            product.name = name
            product.description = description
            product.price = price
            product.stock = stock
            product.is_public = is_public
            product.is_featured = is_featured
            product.in_stock = in_stock
            product.allow_additional_images = allow_additional_images
            product.enable_pixel = enable_pixel
            product.facebook_pixel_id = facebook_pixel_id
            if image:
                product.image = image
            product.save()

        # === Landing Page Config ===
        LandingPageConfig.objects.update_or_create(
            product=product,
            defaults={
                "landing_language": landing_language,
                "layout_direction": layout_direction,
                "enable_feedbacks": enable_feedbacks,
                "enable_related_products": enable_related_products
            }
        )

        # === Additional Images (append-only) ===
        for file_key in request.FILES:
            if file_key.startswith("image_"):
                ProductImage.objects.create(product=product, image=request.FILES[file_key])

        return JsonResponse({
            'success': True,
            'redirect_url': reverse_lazy('dash:products_list')
        })

    else:
        userPlan = UserSubscription.objects.get(user=request.user)
        return render(request, "products/create.html", {"userPlan": userPlan})  # Reuse form page

# Product Update 
@login_required
@role_required(["seller"]) # Assuming only sellers can update their products
def update_product(request, pk):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=pk, user=request.user)
        errors = []

        # Product Fields
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        stock = request.POST.get("stock", "").strip()
        price = request.POST.get("price", "").strip()
        facebook_pixel_id = request.POST.get("facebook_pixel_id", "").strip()

        is_public = bool(request.POST.get("is_public"))
        is_featured = bool(request.POST.get("is_featured"))
        in_stock = bool(request.POST.get("in_stock"))
        allow_additional_images = bool(request.POST.get("allow_additional_images"))
        enable_pixel = bool(request.POST.get("enable_pixel"))

        # Validate required
        if not name:
            errors.append("Product name is required.")
        if not price:
            errors.append("Product price is required.")
        if not stock:
            errors.append("Product stock is required.")

        # Image Upload (optional)
        image = request.FILES.get("image")

        # LandingPageConfig
        landing_language = request.POST.get("landing_language", "ar")
        layout_direction = request.POST.get("layout_direction", "horizontal")
        enable_feedbacks = bool(request.POST.get("enable_feedbacks"))
        enable_related_products = bool(request.POST.get("enable_related_products"))
        if errors:
            return JsonResponse({"success": False, "errors": errors})
        else:
            try:
                with transaction.atomic():
                    # Update Product
                    product.name = name
                    product.description = description
                    product.stock = int(stock or 0)
                    product.price = price
                    product.is_public = is_public
                    product.is_featured = is_featured
                    product.in_stock = in_stock
                    product.allow_additional_images = allow_additional_images
                    product.enable_pixel = enable_pixel
                    product.facebook_pixel_id = facebook_pixel_id or None

                    if image:
                        product.image = image

                    product.full_clean()
                    product.save()

                    # Update LandingPageConfig if exists
                    if hasattr(product, "landing_page"):
                        landing = product.landing_page
                        landing.landing_language = landing_language
                        landing.layout_direction = layout_direction
                        landing.enable_feedbacks = enable_feedbacks
                        landing.enable_related_products = enable_related_products

                        landing.full_clean()
                        landing.save()
                    if product.allow_additional_images:
                        preview_images = request.FILES.getlist("preview_images")
                        for img in preview_images:
                            if img:
                                ProductImage.objects.create(product=product, image=img)

            except ValidationError as ve:
                errors += [f"{field}: {err}" for field, err_list in ve.message_dict.items() for err in err_list]
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'errors' : [str(e)]
                })

        return JsonResponse({"success": True, "redirect_url": reverse("dash:products_list")})

    else: # GET request (Display the form)
        product = get_object_or_404(Product, pk=pk, user=request.user)
        context = {
            "product": product, # Pass the product object for pre-filling
            "language_choices": LandingPageConfig.LANGUAGE_CHOICES, # Needed for dropdown
            "direction_choices": LandingPageConfig.DIRECTION_CHOICES, # Needed for dropdown
        }
    return render(request, "products/update.html", context) # Reuse your existing form template

@login_required
@role_required(["admin","seller"])
def productDetails(request, pk): 
    if request.user.profile.role == "admin":
        product = get_object_or_404(Product, pk=pk)
    else:
        product = get_object_or_404(Product, pk=pk, user=request.user)
    product_images = product.preview_images.all()
    print(product_images)
    return render(request, "products/details.html", {"product": product})

@login_required
@role_required(["admin","seller"])
def Delete(request, pk):
    return BaseDelete(request,Product,pk)



@login_required
@role_required(["admin","seller"])
def DeleteProductImage(request, pk):
    return BaseDelete(request,ProductImage,pk)

