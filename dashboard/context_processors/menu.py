# dashboard/menu.py

from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

menu_items = [
    {
        "name": _("Dashboard"),
        "url": "dash:home",
        "icon": "fas fa-home",
        "roles": ["admin", "seller"]
    },
    {
        "name": _("Users"),
        "url": "dash:users_list",
        "icon": "fas fa-users",
        "roles": ["admin"]
    },
    # ADMIN && SELLER
    {
        "name" : _('Products'),
        "url" : "dash:products_list",
        "icon" : "fas fa-box",
        "roles": ["admin","seller"]
    },
    # ADMIN ONLY
    {
        "name" : _('Subscriptions'),
        "url" : "subs:plans", 
        "icon" : "fas fa-credit-card",
        "roles": ["admin"]
    },
    {
        "name" : _('SMTP Server'),
        "url" : "dash:smtp_config",
        "icon" : "fas fa-envelope",
        "roles": ["admin"]
    },
    {
        "name" : _('Waitlist'),
        "url" : "dash:waitlist",
        "icon" : "fas fa-user-clock",
        "roles": ["admin"]
    },
    {
        "name" : _('Contacts'),
        "url" : "dash:contacts",
        "icon" : "fas fa-address-card",
        "roles": ["admin"]
    },
    {
        "name" : _('Feedbacks'),
        "url" : "dash:feedback_list",
        "icon" : "fas fa-comments",
        "roles": ["admin"]
    },
    {
        "name" : _('Orders'),
        "url" : "dash:orders_list",
        "icon" : "fas fa-box",
        "roles": ["seller"]
    }

]


def get_Menu(request):
    if request.user.is_authenticated:
        context = {
            'menu_items':menu_items
        }
    else :
        context = {
            'menu_items': []
        }
    return context