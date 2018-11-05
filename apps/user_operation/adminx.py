#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:pyy
# datetime:2018/11/5 10:36
import xadmin
from user_operation.models import UserFav, UserLeavingMessage, UserAddress


class UserFavAdmin(object):
    list_display = ['user', 'goods', 'add_time']


class UserLeavingMessageAdmin(object):
    list_dispaly = ['user', 'message_type', 'message', 'add_time']


class UserAddressAdmin(object):
    list_display = ['signer_name', 'signer_mobile', 'district', 'add_time']


xadmin.site.register(UserFav, UserFavAdmin)
xadmin.site.register(UserLeavingMessage, UserLeavingMessageAdmin)
xadmin.site.register(UserAddress, UserAddressAdmin)


