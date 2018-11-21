#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2018/11/20 17:07
from rest_framework import serializers

from goods.models import Goods
from goods.serializer import GoodsSerializer
from trade.models import ShoppingCart


class ShopcartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()
    class Meta:
        model = ShoppingCart
        fields = "__all__"

class ShopcartSerializer(serializers.Serializer):

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, label="数量", min_value=1,
                                    error_messages={
                                        "min_value": "商品数量不能少于1",
                                        "required": "请选择购买商品的数量"
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):
        user = self.context["request"].user
        nums = validated_data['nums']
        goods = validated_data['goods']

        existed = ShoppingCart.objects.filter(user=user, goods=goods)

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        #修改商品数量
        instance.nums = validated_data['nums']
        instance.save()
        return instance
