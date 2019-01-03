# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django Imports
from custom_user.admin import EmailUserAdmin
from django.contrib import admin

# Project Imports
from .models import User
from .forms import UserEditAdminForm,UserCreateAdminForm


class UserAdmin(EmailUserAdmin):
    form = UserEditAdminForm
    add_form = UserCreateAdminForm
    EmailUserAdmin.fieldsets += (
        ('User info', {
            'fields': (
                ('first_name', 'last_name'),
                ('phone_number', 'user_type', 'shop_type'),
                'shop_name',
            )
        }),
    )

    add_fieldsets = EmailUserAdmin.add_fieldsets + (
        ('User info', {
            'fields': (
                ('first_name', 'last_name'),
                ('phone_number', 'user_type', 'shop_type'),
                'shop_name',
            )
        }),
    )


admin.site.register(User, UserAdmin)
