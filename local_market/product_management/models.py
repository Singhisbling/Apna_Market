# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    category_name = models.ForeignKey('Category', on_delete=models.CASCADE)
    sub_category_name = models.CharField(max_length=100)


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    base_price = models.FloatField()
    brand_name = models.CharField(max_length=100)


