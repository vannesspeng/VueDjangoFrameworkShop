#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:pyy
# datetime:2018/11/15 16:58
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from goods.serializer import GoodsSerializer
from user_operation.models import UserFav, UserLeavingMessage, UserAddress


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ('id', 'goods')


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已经收藏该商品！"
            )
        ]
        fields = ('id', 'user', 'goods')


class LeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # read_only=True 表示该字段只存在于返回字段中，不在提交字段中
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserLeavingMessage
        fields = ('user', 'id', 'message_type', 'subject', 'message', 'file', 'add_time')

class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = UserAddress
        fields = ("id", "user", "province", "city", "district", "address", "signer_name", "add_time", "signer_mobile")