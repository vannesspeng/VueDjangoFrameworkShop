from random import choice

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework_jwt.utils import jwt_encode_handler

from goods.models import HotSearchWords
from settings import API_KEY
from users.models import UserProfile, VerifyCode
from users.serializers import SmsSerializer, UserRegSerializer, HotWordsSerializer
from utils.yunpian import Yunpian

User = get_user_model()

class CustomBackend(ModelBackend):
    """
    自定义用户验证函数
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(mobile=username))
            if user and user.check_password(password):
                return user
        except Exception as e:
            return None

class SmsCodeViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = SmsSerializer
    """
        Create a model instance.
    """

    def generate_code(self):
        """
        生产四位数的随机验证码
        :return:
        """
        seeds = "0123456789"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #1、创建随机的验证码
        code = self.generate_code()

        #2、使用云片接口发送验证码到指定的电话号码
        mobile = serializer.data['mobile']
        yun_pian = Yunpian(API_KEY)
        sms_status = yun_pian.send_sms(code, mobile)
        if sms_status['code'] != 0:
            return Response({
                "mobile": sms_status['msg'],
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 3、保存发送验证码记录数据到VerifyCode
            verify_code = VerifyCode(code=code, mobile=mobile)
            verify_code.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)


class UserViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    """
    用户
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data

        payload = jwt_payload_handler(user)
        jwt_token = jwt_encode_handler(payload)

        re_dict['name'] = user.name if user.name else user.username
        re_dict['token'] = jwt_token

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()



class HotSearchsViewset(ListModelMixin, GenericViewSet):
    """
    获取热搜词列表
    """
    queryset = HotSearchWords.objects.all().order_by("-index")
    serializer_class = HotWordsSerializer



