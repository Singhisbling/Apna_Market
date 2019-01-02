# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django Imports
from custom_user.admin import EmailUserAdmin
from django.contrib import admin

# Project Imports
from .models import Shop


class ShopAdmin(EmailUserAdmin):
    EmailUserAdmin.fieldsets += (
        ('User info', {
            'fields': (
                ('first_name', 'last_name'), ('phone_number', 'user_type'),
                'shop_name', ('address1', 'address2'),
                ('country', 'state', 'city'), 'pin_code',
            )
        }),
    )

    add_fieldsets = EmailUserAdmin.add_fieldsets + (
        ('User info', {
            'fields': (
                ('first_name', 'last_name'), ('phone_number', 'user_type'),
                'shop_name', ('address1', 'address2'),
                ('country', 'state', 'city'), 'pin_code',
            )
        }),
    )


admin.site.register(Shop, ShopAdmin)
