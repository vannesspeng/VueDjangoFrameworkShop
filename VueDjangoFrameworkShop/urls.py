"""VueDjangoFrameworkShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from rest_framework.documentation import include_docs_urls


import xadmin
from goods.views import GoodsListViewSet, CategorysListViewSet, BannerViewSet
from .settings import MEDIA_ROOT

from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from trade.views import ShopcartViewset, OrderViewSet, AlipayView
from user_operation.views import UserFavViewSet, LeavingMessageViewset, AddressViewset
from users.views import SmsCodeViewSet, UserViewSet, HotSearchsViewset

router = DefaultRouter()
router.register('goods', GoodsListViewSet, base_name='goods')
router.register('categorys', CategorysListViewSet, base_name='categorys')
router.register('code', SmsCodeViewSet, base_name='code')
router.register('users', UserViewSet, base_name='users')
# 热搜词
router.register('hotsearchs', HotSearchsViewset, base_name="hotsearchs")

#用户收藏
router.register('userfavs', UserFavViewSet, base_name='userfavs')
#用户留言
router.register('messages', LeavingMessageViewset, base_name='messages')
#用户收货地址管理
router.register('address', AddressViewset, base_name='address')
#购物车
router.register('shopcarts', ShopcartViewset, base_name='shopcarts')
router.register('orders', OrderViewSet, base_name='orders')
# 轮播图
router.register('banners', BannerViewSet, base_name='banners')
# goods_list = GoodsListViewSet.as_view({
#     'get': 'list'
# })

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    # 富文本相关url
    path('ueditor/', include('DjangoUeditor.urls')),
    # 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    path('api-auth/', include('rest_framework.urls')),
    path('docs/', include_docs_urls(title="生鲜超市")),
    path('', include(router.urls)),
    # drf自带的token授权登录,获取token需要向该地址post数据
    path('login/', obtain_jwt_token),
    # 支付宝支付相关接口
    path('alipay/return/', AlipayView.as_view()),
    path('index/', TemplateView.as_view(template_name='index.html'), name='index')
]
