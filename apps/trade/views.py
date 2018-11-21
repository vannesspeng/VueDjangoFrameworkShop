from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, authentication, permissions, mixins
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from trade.models import ShoppingCart, OrderInfo, OrderGoods
from trade.serializers import ShopcartSerializer, ShopcartDetailSerializer, OrderSerializer, OrderDetailSerializer
from utils.permissions import IsOwnerOrReadOnly


class ShopcartViewset(viewsets.ModelViewSet):
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    lookup_field = 'goods_id'

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ShopcartDetailSerializer
        else:
            return ShopcartSerializer

class OrderViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    """
    订单管理
    list:
        获取个人订单
    delete:
        删除订单
    create:
        新增订单
    """
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)
    # serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        else:
            return OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)

        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()
            shop_cart.delete()
        return order



