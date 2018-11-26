#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2018/11/6 15:28
from rest_framework import serializers

from goods.models import Goods, GoodsCategory, GoodsImage, Banner


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"

class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image", )

class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images  = GoodsImageSerializer(many=True)
    class Meta:
        model = Goods
        #fields = ('name', 'goods_front_image', 'add_time', 'market_price')
        fields = "__all__"


#第三层级分类
class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"

#第二层级的分类
class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"

# 第一层级分类
class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"