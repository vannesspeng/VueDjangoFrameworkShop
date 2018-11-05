#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2018/11/5 12:40
import xadmin
from trade.models import ShoppingCart, OrderInfo


class ShoppingCartAdmin(object):
    list_display = ['user', 'goods', 'goods_num']

class OrderInfoAdmin(object):
    list_display = ["user", "order_sn", "trade_no", "pay_status", "post_script", "order_mount",
                    "order_mount", "pay_time", "add_time"]

xadmin.site.register(ShoppingCart, ShoppingCartAdmin)
xadmin.site.register(OrderInfo, OrderInfoAdmin)