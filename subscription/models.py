from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=20, unique=True)
    code = models.SlugField(max_length=30, unique=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    max_orders = models.PositiveBigIntegerField(default=30)
    max_products = models.PositiveBigIntegerField(default=1)
    can_export = models.BooleanField(default=False)
    email_support = models.BooleanField(default=False)
    can_import = models.BooleanField(default=False)
    has_analytics = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while SubscriptionPlan.objects.filter(code=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.code = slug
        super().save(*args, **kwargs)

    def get_features(self):
        from django.utils.translation import gettext_lazy as _
        return [
            {
                'name': _('Max Orders'),
                'value': self.max_orders,
                'display': f"{self.max_orders} {_('orders per month')}",
                'enabled': True
            },
            {
                'name': _('Max Products'),
                'value': self.max_products,
                'display': f"{self.max_products} {_('products')}",
                'enabled': True
            },
            {
                'name': _('Data Export'),
                'value': self.can_export,
                'display': _('Data export'),
                'enabled': self.can_export
            },
            {
                'name': _('Data Import'),
                'value': self.can_import,
                'display': _('Data import'),
                'enabled': self.can_import
            },
            {
                'name': _('Email Support'),
                'value': self.email_support,
                'display': _('Email support'),
                'enabled': self.email_support
            },
            {
                'name': _('Advanced Analytics'),
                'value': self.has_analytics,
                'display': _('Advanced analytics'),
                'enabled': self.has_analytics
            }
        ]


class UserSubscription(models.Model):
    """Model tracking user access limits based on usage"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sub')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    start_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"

    def can_add_order(self):
        return self.user.orders.count() < self.plan.max_orders

    def can_add_product(self):
        return self.user.products.count() < self.plan.max_products

    def reached_order_limit(self):
        return not self.can_add_order()

    def reached_product_limit(self):
        return not self.can_add_product()

    @property
    def orders_used(self):
        return self.user.orders.count()

    @property
    def products_used(self):
        return self.user.products.count()
