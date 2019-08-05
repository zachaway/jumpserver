# coding: utf-8
#

from common.serializers import AdaptedBulkListSerializer
from orgs.mixins import BulkOrgResourceModelSerializer
from ..models import Database

__all__ = ['DatabaseSerializer']


class DatabaseSerializer(BulkOrgResourceModelSerializer):
    class Meta:
        model = Database
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            'id', 'name', 'login_mode', 'type', 'host', 'port', 'user',
            'password', 'database', 'created_by', 'date_created',
            'date_updated', 'comment',
        ]

        read_only_fields = [
            'created_by', 'date_created', 'date_updated'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    @staticmethod
    def clean_password(validated_data):
        password = validated_data.get('password')
        if not password:
            validated_data.pop('password', None)

    def create(self, validated_data):
        self.clean_password(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self.clean_password(validated_data)
        return super().update(instance, validated_data)

