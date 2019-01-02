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


class Shop(AbstractEmailUser):
    # Attributes

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    user_type = models.CharField(
        choices=USER_TYPE, max_length=30
    )
    shop_name = models.CharField(max_length=250)

    phone_number = PhoneNumberField(
        blank=True, help_text=u'Contact phone number. '
                              u'The number should be in the format '
                              u'+(country code)(number)x(extension) where the '
                              u'extension part is optional.'
    )
    address1 = models.CharField(max_length=500)
    address2 = models.CharField(max_length=500, blank=True, null=True)
    country = CountryField()
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pin_code = models.CharField(max_length=15)

