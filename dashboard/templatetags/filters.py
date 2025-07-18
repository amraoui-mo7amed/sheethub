from django import template
import hashlib
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def md5(value):
    return hashlib.md5(value.encode('utf-8')).hexdigest()

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
    

@register.filter
def format_revenue(value):
    """
    Format revenue numbers with k/m suffixes
    - Numbers >= 1,000,000: display as 1m, 16m, etc.
    - Numbers >= 1,000: display as 1k, 16k, etc.
    - Numbers < 1,000: display as is
    """
    try:
        value = float(value)
    except (ValueError, TypeError):
        return value
    
    if value >= 1_000_000:
        # Format as millions
        millions = value / 1_000_000
        return f"{millions:.0f}m"
    elif value >= 1_000:
        # Format as thousands
        thousands = value / 1_000
        return f"{thousands:.0f}k"
    else:
        # Display as is for numbers less than 1000
        return f"{value:.0f}"

