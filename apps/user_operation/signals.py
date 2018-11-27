#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2018/11/27 16:13

# post_save:接收信号的方式
#sender: 接收信号的model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from user_operation.models import UserFav


@receiver(post_save, sender=UserFav)
def create_userfav(sender, instance=None, created=False, **kwargs):
    # 是否新建，因为update的时候也会进行post_save,只有新增的时候，created才为True
    if created:
        goods = instance.goods
        #instance相当于user
        goods.fav_num += 1
        goods.save()


@receiver(post_delete, sender=UserFav)
def delete_userfav(sender, instance=None, created=False, **kwargs):
    # 是否新建，因为update的时候也会进行post_save
    goods = instance.goods
    #instance相当于user
    goods.fav_num -= 1
    goods.save()