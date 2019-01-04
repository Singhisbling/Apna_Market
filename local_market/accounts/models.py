# Python Imports
from __future__ import unicode_literals

# Django Imports
from custom_user.models import AbstractEmailUser
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


USER_TYPE = (
    ('buyer', 'Buyer'),
    ('seller', 'Seller'),
)

SELLER_TYPE = (
    ('Grocery', 'GROCERY'),
    ('clothing', 'CLOTHING'),
    ('automobiles', 'AUTOMOBILES'),
    ('construction and building materials', 'CONSTRUCTION AND BUILDING MATERIALS'),
)


class User(AbstractEmailUser):
    user_type = models.CharField(
        choices=USER_TYPE, max_length=7
    )

    class Meta:
        verbose_name_plural = "User"
        verbose_name = 'User'


class Buyer(models.Model):
    # Attributes
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    profile_pic = models.ImageField(blank=True, null=True)
    phone_number = PhoneNumberField(
        blank=True, help_text=u'Contact phone number. '
                              u'The number should be in the format '
                              u'+(country code)(number)x(extension) where the '
                              u'extension part is optional.'
    )

    class Meta:
        verbose_name_plural = "Buyer"
        verbose_name = 'Buyer'

    def __str__(self):
        return str(self.user)


class Seller(models.Model):
    # Attributes
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    shop_owner_first_name = models.CharField(max_length=255, blank=True)
    shop_owner_last_name = models.CharField(max_length=255, blank=True)
    shop_owner_profile_pic = models.ImageField(blank=True, null=True)
    shop_owner_phone_number = PhoneNumberField(
        blank=True, help_text=u'Contact phone number. '
                              u'The number should be in the format '
                              u'+(country code)(number)x(extension) where the '
                              u'extension part is optional.'
    )
    shop_type = models.CharField(
        choices=SELLER_TYPE, max_length=255
    )
    shop_name = models.CharField(max_length=255)
    shop_number = models.CharField(max_length=255)
    account_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Seller"
        verbose_name = 'Seller'

    def __str__(self):
        return str(self.user)


class Address(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE,)
    address = models.TextField(max_length=255)
    pin_code = models.IntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = CountryField()


