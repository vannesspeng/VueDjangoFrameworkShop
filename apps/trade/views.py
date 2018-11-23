from datetime import datetime

from django.shortcuts import render, redirect

# Create your views here.
from rest_framework import viewsets, authentication, permissions, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from trade.models import ShoppingCart, OrderInfo, OrderGoods
from trade.serializers import ShopcartSerializer, ShopcartDetailSerializer, OrderSerializer, OrderDetailSerializer
from utils.alipay import AliPay
from utils.permissions import IsOwnerOrReadOnly
from VueDjangoFrameworkShop.settings import ali_pub_key_path, private_key_path


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



class AlipayView(APIView):
    def get(self, reqeust):
        """
        处理支付宝的return_url返回
        :param reqeust:
        :return:
        """
        """
        处理支付宝的return_url返回
        """
        processed_dict = {}
        # 1. 获取GET中参数
        for key, value in reqeust.GET.items():
            processed_dict[key] = value
        # 2. 取出sign
        sign = processed_dict.pop("sign", None)

        # 3. 生成ALipay对象
        alipay = AliPay(
            # appid在沙箱环境中就可以找到
            appid="2016092000553933",
            # 这个值先不管，在与vue的联调中介绍
            app_notify_url="http://39.108.225.222:8000/alipay/return/",
            # 我们自己商户的密钥
            app_private_key_path=private_key_path,
            # 支付宝的公钥
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            # debug为true时使用沙箱的url。如果不是用正式环境的url
            debug=True,  # 默认False,
            # 先不用管，后面vue解释
            return_url="http://39.108.225.222:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            # 将success返回给支付宝，支付宝就不会一直不停的继续发消息了。
            response = redirect("/index/#/app/home/member/order")
            return response
        else:
            response = redirect("index")
            return response

    def post(self, request):
        """
        处理支付宝的notify_url
        :param request:
        :return:
        """
        # 1、先将sign字段剔除
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value
        sign = processed_dict.pop("sign", None)

        # 2、生成一个alipay对象
        alipay = AliPay(
            # appid在沙箱环境中就可以找到
            appid="2016092000553933",
            # 这个值先不管，在与vue的联调中介绍
            app_notify_url="http://39.108.225.222:8000/alipay/return/",
            # 我们自己商户的密钥
            app_private_key_path=private_key_path,
            # 支付宝的公钥
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            # debug为true时使用沙箱的url。如果不是用正式环境的url
            debug=True,  # 默认False,

            # 先不用管，后面vue解释
            return_url="http://39.108.225.222:8000/alipay/return/"
        )

        # 3、进行验签
        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            # 查询数据库中存在的订单
            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                # 订单商品项
                order_goods = existed_order.goods.all()
                # 商品销量增加订单中数值
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_num += order_good.goods_num
                    goods.save()

                # 更新订单状态，填充支付宝给的交易凭证号。
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()
            # 将success返回给支付宝，支付宝就不会一直不停的继续发消息了。
            return Response("success")

