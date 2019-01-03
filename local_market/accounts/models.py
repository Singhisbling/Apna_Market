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
    ('construction and building materials', 'CONSTRUCTION AND BUILDING MATERIALS'),
)


class User(AbstractEmailUser):
    # Attributes
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    user_type = models.CharField(
        choices=USER_TYPE, max_length=30
    )
    shop_type = models.CharField(
        choices=SELLER_TYPE, max_length=100, blank=True, null=True
    )
    shop_name = models.CharField(max_length=250)

    phone_number = PhoneNumberField(
        blank=True, help_text=u'Contact phone number. '
                              u'The number should be in the format '
                              u'+(country code)(number)x(extension) where the '
                              u'extension part is optional.'
    )
    account_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "User"
        verbose_name = 'User'


class Shop(models.Model):
    pass


class Address(models.Model):
    pass


