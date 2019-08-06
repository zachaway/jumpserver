# coding: utf-8
#

from rest_framework import serializers

from common.serializers import AdaptedBulkListSerializer
from orgs.mixins import BulkOrgResourceModelSerializer
from ..models import Database

__all__ = ['DatabaseSerializer', 'DatabaseAuthInfoSerializer']


class DatabaseSerializer(BulkOrgResourceModelSerializer):
    type_display = serializers.ReadOnlyField(source='get_type_display')
    login_mode_display = serializers.ReadOnlyField(source='get_login_mode_display')

    class Meta:
        model = Database
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            'id', 'name', 'login_mode', 'type', 'host', 'port', 'user',
            'password', 'database', 'created_by', 'date_created',
            'date_updated', 'comment',
            'type_display', 'login_mode_display'
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


class DatabaseAuthInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Database
        fields = ['password']
