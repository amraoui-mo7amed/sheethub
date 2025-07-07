from django.urls import reverse_lazy, reverse
from .generic import *
from dashboard.mixins import AdminRequiredMixin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from dashboard.decorators import role_required, admin_required, user_is_self
from dashboard.models import Product, ProductImage
from utils import loadJSON

userModel = get_user_model()

@login_required
@role_required(["seller"])
def list(request): 
    Products = Product.objects.filter(user=request.user)
    return render(request, "products/list.html", {"products": Products})

@login_required
def create(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "products/create.html")