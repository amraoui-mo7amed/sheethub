from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    max_orders = models.PositiveBigIntegerField(default=30)
    max_products = models.PositiveBigIntegerField(default=5)
    can_export = models.BooleanField(default=False)
    email_support = models.BooleanField(default=False)
    can_import = models.BooleanField(default=False)
    has_analytics = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
        
    def get_features(self):
        """
        Returns a list of dictionaries containing all features of the plan.
        Each feature has a name, value, and whether it's enabled.
        """
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
    """Model tracking user subscriptions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"