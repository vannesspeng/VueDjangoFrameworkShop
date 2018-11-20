from django.shortcuts import render

# Create your views here.
from rest_framework import authentication
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from user_operation.models import UserFav, UserLeavingMessage, UserAddress
from user_operation.serializers import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer, \
    AddressSerializer
from utils.permissions import IsOwnerOrReadOnly



class UserFavViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)
    serializer_class = UserFavSerializer
    lookup_field = 'goods_id'

    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer
        elif self.action == 'create':
            return UserFavSerializer

        return UserFavSerializer

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

class LeavingMessageViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                            mixins.DestroyModelMixin):
    """
    list:
        获取用户留言
    create:
        添加留言
    delete:
        删除留言
    """
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)
    serializer_class = LeavingMessageSerializer

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)

# viewsets.ModelViewSet实现了所有增删改查的功能
class AddressViewset(viewsets.ModelViewSet):
    """
    list:
        获取用户留言
    create:
        添加留言
    delete:
        删除留言
    """
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)
    serializer_class = AddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

