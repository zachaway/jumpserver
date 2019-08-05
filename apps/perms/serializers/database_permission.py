#  coding: utf-8
#

from rest_framework import serializers

from common.serializers import AdaptedBulkListSerializer
from orgs.mixins import BulkOrgResourceModelSerializer
from ..models import DatabasePermission


__all__ = [
    'DatabasePermissionSerializer',
    'DatabasePermissionUpdateUserSerializer',
    'DatabasePermissionUpdateDatabaseSerializer'
]


class DatabasePermissionSerializer(BulkOrgResourceModelSerializer):
    class Meta:
        model = DatabasePermission
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            'id', 'name', 'users', 'user_groups', 'databases', 'comment',
            'is_active', 'date_start', 'date_expired', 'is_valid',
            'created_by', 'date_created',
        ]
        read_only_fields = ['created_by', 'date_created']


class DatabasePermissionUpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabasePermission
        fields = ['id', 'users']


class DatabasePermissionUpdateDatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabasePermission
        fields = ['id', 'databases']

