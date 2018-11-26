from django.shortcuts import render
from django.views.generic.base import View


# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import  filters
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet

from goods.filters import GoodsFilter
from .serializer import GoodsSerializer, CategorySerializer, BannerSerializer
from .models import Goods, GoodsCategory, Banner


class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100

# class GoodsListView(ListAPIView):
#     """
#     通过django的view实现商品列表
#     :param request:
#     :return:
#     """
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     pagination_class = GoodsPagination

class GoodsListViewSet(ListModelMixin, RetrieveModelMixin ,GenericViewSet):
    # 商品列表页：分页、搜索、过滤、排序
    queryset = Goods.objects.all().order_by('id')
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    filter_backends = (DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ['name', 'goods_brief', 'goods_desc']
    ordering_fields = ['sold_num', 'add_time', 'shop_price']


    # 进行简单的过滤
    # def get_queryset(self):
    #     self.queryset =  Goods.objects.filter(shop_price__gt=220)
    #     return self.queryset


class CategorysListViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class BannerViewSet(GenericViewSet, ListModelMixin):
    """
        获取轮播图列表
        """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer




