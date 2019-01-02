# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Category,SubCategory,Product

# Register your models here.


class SubCategoryAdmin(admin.TabularInline):
    model = SubCategory
    fields = ('category_name', 'sub_category_name')
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    inlines = [SubCategoryAdmin]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)
