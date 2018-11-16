from django.shortcuts import render

# Create your views here.
from rest_framework.authentication import SessionAuthentication
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from user_operation.models import UserFav
from user_operation.serializers import UserFavSerializer
from utils.permissions import IsOwnerOrReadOnly



class UserFavViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    serializer_class = UserFavSerializer
    lookup_field = 'goods_id'

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)