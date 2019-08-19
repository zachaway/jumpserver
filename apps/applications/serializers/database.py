# coding: utf-8
#

from common.serializers import AdaptedBulkListSerializer
from orgs.mixins import BulkOrgResourceModelSerializer
from ..models import Database

__all__ = ["DatabaseSerializer"]


class DatabaseSerializer(BulkOrgResourceModelSerializer):
    class Meta:
        model = Database
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            'id', 'name', 'login_mode', 'type',
            'host', 'port', 'user', 'password', 'database',
            'comment', 'created_by', 'date_created', 'date_updated',
        ]
        read_only_fields = [
            'created_by', 'date_created', 'date_updated'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }
