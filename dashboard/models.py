from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

userModel = get_user_model()

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

class SMTPConfig(models.Model):
    """Singleton model for SMTP configuration"""
    host = models.CharField(max_length=255, default='smtp.gmail.com')
    port = models.IntegerField(default=587)
    use_tls = models.BooleanField(default=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    from_email = models.EmailField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"SMTP: {self.host}"

class Notification(models.Model):
    user = models.ForeignKey(userModel, on_delete=models.CASCADE,related_name=_("notifications"))
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        ordering = ["-created_at"]

class Product(models.Model):
    user = models.ForeignKey(userModel, on_delete=models.CASCADE, related_name=_("products"), blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    stock = models.PositiveBigIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    
    # NEW FIELDS
    is_public = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=True)
    allow_additional_images = models.BooleanField(default=False)
    enable_pixel = models.BooleanField(default=False)
    facebook_pixel_id = models.CharField(max_length=32, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def preview_images_list(self):
        return self.preview_images.all()[:4]

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='preview_images'
    )
    image = models.ImageField(upload_to='products/previews/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Preview for {self.product.name}"

class LandingPageConfig(models.Model):
    LANGUAGE_CHOICES = [
        ('ar', 'Arabic'),
        ('en', 'English'),
        ('fr', 'French'),
    ]
    DIRECTION_CHOICES = [
        ('horizontal', 'Horizontal'),
        ('vertical', 'Vertical'),
    ]

    product = models.OneToOneField("Product", on_delete=models.CASCADE, related_name="landing_page")
    landing_language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='ar')
    layout_direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES, default='horizontal')
    enable_feedbacks = models.BooleanField(default=True)
    enable_related_products = models.BooleanField(default=True)

    def __str__(self):
        return f"Landing config for {self.product.name}"
