# coding: utf-8
#

from rest_framework.pagination import LimitOffsetPagination
from rest_framework_bulk import BulkModelViewSet

from ..hands import IsOrgAdmin
from ..models import Database
from ..serializers import DatabaseSerializer

__all__ = ['DataBaseViewSet']


class DataBaseViewSet(BulkModelViewSet):
    filter_fields = ('name',)
    search_fields = filter_fields
    permission_classes = (IsOrgAdmin,)
    queryset = Database.objects.all()
    serializer_class = DatabaseSerializer
    pagination_class = LimitOffsetPagination
