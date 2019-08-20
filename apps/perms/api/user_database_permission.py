# coding: utf-8
#

from django.shortcuts import get_object_or_404

from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from common.tree import TreeNodeSerializer
from common.permissions import IsOrgAdminOrAppUser, IsValidUser

from ..hands import User, DatabaseSerializer
from ..utils import (
    DatabasePermissionUtil,
    construct_databases_tree_root,
    parse_database_to_tree_node,
)
from ..mixins import DatabaseFilterMixin

__all__ = ['UserGrantedDatabasesApi', 'UserGrantedDatabasesAsTreeApi']


class UserGrantedDatabasesApi(DatabaseFilterMixin, ListAPIView):
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


class UserGrantedDatabasesAsTreeApi(ListAPIView):
    serializer_class = TreeNodeSerializer
    permission_classes = (IsOrgAdminOrAppUser,)

    def get_object(self):
        user_id = self.kwargs.get('pk', '')
        if not user_id:
            user = self.request.user
        else:
            user = get_object_or_404(User, id=user_id)
        return user

    def get_queryset(self):
        queryset = []
        tree_root = construct_databases_tree_root()
        queryset.append(tree_root)

        util = DatabasePermissionUtil(self.get_object())
        databases = util.get_databases()
        for database in databases:
            node = parse_database_to_tree_node(tree_root, database)
            queryset.append(node)
        queryset = sorted(queryset)
        return queryset

    def get_permissions(self):
        if self.kwargs.get('pk') is None:
            self.permission_classes = (IsValidUser,)
        return super().get_permissions()
