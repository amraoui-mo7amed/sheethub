from .generic import *
from dashboard.mixins import AdminRequiredMixin
from dashboard.decorators import admin_required
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from utils import loadJSON

userModel = get_user_model()


class list( AdminRequiredMixin ,BaseListView):
    model = userModel 
    template_name = "users/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objects'] = userModel.objects.all().exclude(is_staff=True)
        return context

@admin_required
def Delete(request, pk):
    return BaseDelete(request,userModel,pk)

def userProfile(request, pk):
    user = get_object_or_404(userModel, pk=pk)
    context = {
        'user' : user
    }
    return render(request, 'users/profile.html', context = context)