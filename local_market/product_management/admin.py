# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Category,SubCategory,Product,SubSubCategory

# Register your models here.


class SubSubCategoryAdmin(admin.TabularInline):
    model = SubSubCategory
    fields = ('sub_category_name', 'sub_sub_category_name')
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    model = Category


class SubCategoryAdmin(admin.ModelAdmin):
    model = SubCategory
    fields = ('category_name', 'sub_category_name')
    inlines = [SubSubCategoryAdmin]
    extra = 0


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product)
