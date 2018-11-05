#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2018/11/2 11:07
import xadmin
from xadmin import views
from users.models import VerifyCode


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    site_title = "生鲜超市"
    site_footer = "supermarket.com"

class VerifyCodeAdmin(object):
    list_display = ['code', 'mobile', 'add_time']


xadmin.site.register(VerifyCode, VerifyCodeAdmin)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(views.BaseAdminView, BaseSetting)