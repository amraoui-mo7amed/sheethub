from unicodedata import category
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        user = self.create_user(email, password, **extra_fields)
        # Create UserAuth with email_confirmed=True for superuser
        UserAuth.objects.create(user=user, email_confirmed=True)
        return user

class CustomUser(AbstractUser):
    # Replace username with email as the unique identifier
    email = models.EmailField(unique=True)
    username = None  # Remove the username field

    # Required for custom user model
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Fields required when creating a user via createsuperuser

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class UserAuth(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='auth')
    # Email confirmation fields
    email_confirmed = models.BooleanField(default=False)
    email_confirmation_token = models.CharField(max_length=100, blank=True, null=True)
    email_confirmation_sent = models.DateTimeField(null=True, blank=True)
    
    # Password reset fields
    password_reset_token = models.CharField(max_length=100, blank=True, null=True)
    password_reset_sent = models.DateTimeField(null=True, blank=True)
    

    def __str__(self):
        return f"Auth Info for User {self.user.id}"

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', _('Admin')), 
        ('seller' , _('Seller'))
    ]
    # Algerian provinces
    ALGERIAN_PROVINCES = [
        ('adrar', 'Adrar'), ('chlef', 'Chlef'), ('laghouat', 'Laghouat'),
        ('oum_el_bouaghi', 'Oum El Bouaghi'), ('batna', 'Batna'),
        ('bejaia', 'Béjaïa'), ('biskra', 'Biskra'), ('bechar', 'Béchar'),
        ('blida', 'Blida'), ('bouira', 'Bouira'), ('tamanghasset', 'Tamanrasset'),
        ('tebessa', 'Tébessa'), ('tlemcen', 'Tlemcen'), ('tiaret', 'Tiaret'),
        ('tizi_ouzou', 'Tizi Ouzou'), ('alger', 'Alger'), ('djelfa', 'Djelfa'),
        ('jijel', 'Jijel'), ('setif', 'Sétif'), ('saida', 'Saïda'),
        ('skikda', 'Skikda'), ('sidi_bel_abbes', 'Sidi Bel Abbès'),
        ('annaba', 'Annaba'), ('guelma', 'Guelma'), ('constantine', 'Constantine'),
        ('medea', 'Médéa'), ('mostaganem', 'Mostaganem'), ('msila', 'M\'Sila'),
        ('mascara', 'Mascara'), ('ouargla', 'Ouargla'), ('oran', 'Oran'),
        ('el_bayadh', 'El Bayadh'), ('illizi', 'Illizi'), ('bordj_bou_arreridj', 'Bordj Bou Arréridj'),
        ('boumerdes', 'Boumerdès'), ('el_tarf', 'El Tarf'), ('tindouf', 'Tindouf'),
        ('tissemsilt', 'Tissemsilt'), ('el_oued', 'El Oued'), ('khenchela', 'Khenchela'),
        ('souk_ahras', 'Souk Ahras'), ('tipaza', 'Tipaza'), ('mila', 'Mila'),
        ('ain_defla', 'Aïn Defla'), ('naama', 'Naâma'), ('ain_temouchent', 'Aïn Témouchent'),
        ('ghardaia', 'Ghardaïa'), ('relizane', 'Relizane')
    ]

    ECOMMERCE_CATEGORIES = [
        ('electronics', _('Electronics')),
        ('fashion', _('Fashion')),
        ('home_garden', _('Home & Garden')),
        ('beauty', _('Beauty & Personal Care')),
        ('sports', _('Sports & Outdoors')),
        ('toys', _('Toys & Games')),
        ('food', _('Food & Groceries')),
        ('health', _('Health & Wellness')),
        ('automotive', _('Automotive')),
        ('books', _('Books & Media')),
        ('pets', _('Pet Supplies')),
        ('office', _('Office Supplies')),
        ('jewelry', _('Jewelry & Watches')),
        ('baby', _('Baby Products')),
        ('industrial', _('Industrial & Scientific'))
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile', verbose_name=_('user'))
    role = models.CharField(_('role'), max_length=11, choices=ROLE_CHOICES, default='seller')
    phone_number = models.CharField(_('phone number'), max_length=20, blank=True, null=True)
    province = models.CharField(_('province'), max_length=50, choices=ALGERIAN_PROVINCES, blank=True, null=True)
    category = models.CharField(_('business category'), max_length=50, choices=ECOMMERCE_CATEGORIES, blank=True, null=True)
    max_orders = models.IntegerField(_('max orders'), default=1)
    available_orders = models.IntegerField(_('available orders'), default=1)
    max_products = models.IntegerField(_('max products'), default=1)
    available_products = models.IntegerField(_('available products'), default=1)

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')

    def __str__(self):
        return f"{self.user.email}'s profile"