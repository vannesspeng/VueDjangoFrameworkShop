from datetime import datetime                      #1、首先import 系统包

from django.contrib.auth.models import AbstractUser#2、然后import第三方包
from django.db import models                       #3、最后导入项目自身模块的包



class UserProfile(AbstractUser):
    """
    用户实体
    """

    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="female",
                              verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="电子邮箱")

    class Meta:
        verbose_name = "用户"
        # model的复数形式
        verbose_name_plural = verbose_name
        app_label = 'users'

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    """
    短信验证码，回填验证码进行验证。可以保存在redis中
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
