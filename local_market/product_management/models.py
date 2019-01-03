# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

GENDER_TYPE = (
    ('male', 'Male'),
    ('female', 'Female'),
)


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    category_name = models.ForeignKey('Category', on_delete=models.CASCADE)
    sub_category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.sub_category_name)


class SubSubCategory(models.Model):
    sub_category_name = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    sub_sub_category_name = models.CharField(max_length=100)


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    base_price = models.FloatField()
    brand_name = models.CharField(max_length=100)
    gender = models.CharField(
        choices=GENDER_TYPE, max_length=100
    )


class TopWearClothingProduct(Product):
    neck_type = models.CharField(
        choices=GENDER_TYPE, max_length=100
    )



