from django.db import models
from django.utils import timezone
from django.db.models import Sum, Count, F, FloatField
from utils import loadJSON
from django.utils.translation import gettext_lazy as _

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('shipped', _('Shipped')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    ]

    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    wilaya = models.CharField(max_length=100)
    commune = models.CharField(max_length=100)

    product = models.ForeignKey('dashboard.Product', on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField(default=1)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_confirmed = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.product.name} ({self.quantity})"

    @property
    def total_price(self):
        return self.quantity * self.product.price

    @classmethod
    def get_order_stats(cls, status_filter=None):
        qs = cls.objects.all()
        if status_filter:
            qs = qs.filter(status=status_filter)

        return qs.aggregate(
            total_orders=Count('id'),
            total_revenue=Sum(F('quantity') * F('product__price'), output_field=FloatField())
        )


    @property
    def wilaya_display(self):
        try:
            algeria = loadJSON('algeria.json')
            # Normalize code with leading zero
            code = str(int(self.wilaya)).zfill(2)
            for entry in algeria:
                if entry["wilaya_code"] == code:
                    return entry["wilaya_name_ascii"]
        except Exception:
            pass
        return self.wilaya  # fallback: raw code
