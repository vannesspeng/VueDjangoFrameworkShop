#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:pyy
# datetime:2018/11/7 16:47
from django.db.models import Q

from goods.models import Goods
from django_filters import rest_framework as filters


class GoodsFilter(filters.FilterSet):
    pricemin = filters.NumberFilter(field_name='shop_price', lookup_expr='gte')
    pricemax = filters.NumberFilter(field_name='shop_price', lookup_expr='lte')
    top_category = filters.NumberFilter(name="category", method="top_category_filter")

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax']
