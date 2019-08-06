# coding: utf-8
#

from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_bulk import BulkModelViewSet

from ..hands import IsOrgAdmin, IsAppUser
from ..models import Database
from ..serializers import DatabaseSerializer, DatabaseAuthInfoSerializer

__all__ = ['DataBaseViewSet', 'DatabaseAuthInfoApi']


class DataBaseViewSet(BulkModelViewSet):
    filter_fields = ('name',)
    search_fields = filter_fields
    permission_classes = (IsOrgAdmin,)
    queryset = Database.objects.all()
    serializer_class = DatabaseSerializer
    pagination_class = LimitOffsetPagination


class DatabaseAuthInfoApi(generics.RetrieveAPIView):
    queryset = Database.objects.all()
    permission_classes = (IsAppUser,)
    serializer_class = DatabaseAuthInfoSerializer
