# coding: utf-8
#


from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView

from rest_framework.pagination import LimitOffsetPagination

from common.permissions import IsOrgAdminOrAppUser, IsValidUser
from ..hands import User, DatabaseSerializer
from ..utils import (
    DatabasePermissionUtil,
)
from ..mixins import DatabasesFilterMixin

__all__ = [
    'UserGrantedDatabasesApi',
]


class UserGrantedDatabasesApi(DatabasesFilterMixin, ListAPIView):
    permission_classes = (IsOrgAdminOrAppUser,)
    serializer_class = DatabaseSerializer
    pagination_class = LimitOffsetPagination

    def get_object(self):
        user_id = self.kwargs.get('pk', '')
        if user_id:
            user = get_object_or_404(User, id=user_id)
        else:
            user = self.request.user
        return user

    def get_queryset(self):
        util = DatabasePermissionUtil(self.get_object())
        queryset = util.get_databases()
        queryset = list(queryset)
        return queryset

    def get_permissions(self):
        if self.kwargs.get('pk') is None:
            self.permission_classes = (IsValidUser,)
        return super().get_permissions()
