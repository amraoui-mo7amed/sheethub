from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class WaitList(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.fullname
    
    class Meta:
        verbose_name = _("Waitlist")
        verbose_name_plural = _("Waitlist")
        ordering = ["-created_at"]