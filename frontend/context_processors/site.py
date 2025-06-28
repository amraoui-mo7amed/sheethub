from django.conf import settings
from django.utils.translation import gettext_lazy as _
from subscription.models import SubscriptionPlan

def site_details(request):
    """
    Context processor that provides site-wide information.
    These variables will be available in all templates.
    """
    return {
        'plans' : SubscriptionPlan.objects.all() or [],
        "contact" : {}
    }