# coding: utf-8
#

from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from common.permissions import IsOrgAdmin
from ..models import DatabasePermission
from ..serializers import DatabasePermissionSerializer

__all__ = ['DatabasePermissionViewSet']


class DatabasePermissionViewSet(viewsets.ModelViewSet):
    filter_fields = ('name',)
    search_fields = filter_fields
    queryset = DatabasePermission.objects.all()
    serializer_class = DatabasePermissionSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsOrgAdmin,)
