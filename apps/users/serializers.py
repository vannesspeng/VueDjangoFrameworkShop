#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:pyy
# datetime:2018/11/13 10:15
import re
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from goods.models import HotSearchWords
from VueDjangoFrameworkShop.settings import REGEX_MOBILE
from users.models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码函数（函数名必须为valite_ + 字段名）
        :param mobile:
        :return:
        """
        # 1、验证手机号码是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 2、验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码格式错误")
        # 3、验证码发送频率
        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, mobile=mobile):
            raise serializers.ValidationError("距离上一次发送验证码不足60秒")

        return mobile


class UserDetailSerializer(serializers.ModelSerializer):
    """
       用户详情序列化
    """
    class Meta:
        model = User
        fields = ("username", "gender", "birthday", "email", "mobile", "name")


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, max_length=4, min_length=4,
                                 error_messages={
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误",
                                     "blank": "请输入验证码"
                                 },
                                 help_text="验证码",
                                 write_only=True)
    username = serializers.CharField(required=True, allow_blank=False, error_messages={"blank": "请输入用户名"},
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在！")])
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    def validate_code(self, code):

        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if verify_records:
            last_record = verify_records[0]
            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minutes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

        # 不加字段名的验证器作用于所有字段之上。attrs是字段 validate之后返回的总的dict

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")


class HotWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSearchWords
        fields = "__all__"
