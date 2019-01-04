# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django Imports
from custom_user.admin import EmailUserAdmin
from django.contrib import admin

# Project Imports
from .models import User, Buyer, Seller


class UserAdmin(EmailUserAdmin):
    list_display = ['email', 'user_type']
    EmailUserAdmin.fieldsets += (
        ('User info', {
            'fields': (
                ('email', 'user_type'),
            )
        }),
    )

    add_fieldsets = EmailUserAdmin.add_fieldsets + (
        ('User info', {
            'fields': (
                ('email', 'user_type'),
            )
        }),
    )


class BuyerAdmin(admin.ModelAdmin):
    model = Buyer
    fieldsets = (
        ('User', {
            'fields': ('user',)}),
        ('Profile Picture', {
            'fields': ('profile_pic', )}),
        ('Owner Name', {
            'fields': ('first_name', 'last_name')}),
        ('Phone Number', {
            'fields': ('phone_number', )}),
    )


class SellerAdmin(admin.ModelAdmin):
    model = Seller
    fieldsets = (
        ('User', {
            'fields': ('user',)}),
        ('Profile Picture', {
            'fields': ('shop_owner_profile_pic', )}),
        ('Owner Name', {
            'fields': ('shop_owner_first_name', 'shop_owner_last_name')}),
        ('Phone Number', {
            'fields': ('shop_owner_phone_number', )}),
        ('Shop', {
            'fields': ('shop_type', 'shop_name', 'shop_number')}),
        ('Account Verified', {
            'fields': ('account_verified', )}),
        )


admin.site.register(Buyer, BuyerAdmin)
admin.site.register(Seller, SellerAdmin)
admin.site.register(User, UserAdmin)
