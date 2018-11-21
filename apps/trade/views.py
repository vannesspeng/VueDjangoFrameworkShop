from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, authentication, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from trade.models import ShoppingCart
from trade.serializers import ShopcartSerializer, ShopcartDetailSerializer
from utils.permissions import IsOwnerOrReadOnly


class ShopcartViewset(viewsets.ModelViewSet):
    # serializer_class = ShopcartSerializer
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



