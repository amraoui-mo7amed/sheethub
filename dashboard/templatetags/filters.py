from django import template
import hashlib

register = template.Library()

@register.filter
def md5(value):
    return hashlib.md5(value.encode('utf-8')).hexdigest()

import hashlib
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def gravatar(email, size=80):
    """Generate Gravatar URL for a given email."""
    email_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d=identicon"

@register.filter
def percentage(value, total):
    try:
        return (float(value) / float(total)) * 100
    except (ValueError, ZeroDivisionError):
        return 0
    


