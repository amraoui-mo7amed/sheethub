from .generic import BaseDelete, BaseListView
from dashboard.models import WaitList
from django.utils.translation import gettext_lazy as _
from dashboard.decorators import admin_required
from dashboard.mixins import AdminRequiredMixin


class List(AdminRequiredMixin, BaseListView):
    model = WaitList
    template_name = "waitlist/list.html"
    