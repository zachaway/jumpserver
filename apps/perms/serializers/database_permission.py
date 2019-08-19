# coding: utf-8
#

from rest_framework import serializers

from orgs.mixins import BulkOrgResourceModelSerializer

from common.serializers import AdaptedBulkListSerializer
from ..models import DatabasePermission

__all__ = [
    'DatabasePermissionSerializer',
    'DatabasePermissionUpdateUserSerializer',
    'DatabasePermissionUpdateDatabaseSerializer',
]


class DatabasePermissionSerializer(BulkOrgResourceModelSerializer):
    class Meta:
        model = DatabasePermission
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            'id', 'name', 'users', 'user_groups', 'databases',
            'is_active', 'is_valid', 'comment',
            'date_start', 'date_expired', 'date_created', 'created_by',
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
