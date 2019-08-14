# ~*~ coding: utf-8 ~*~
from rest_framework import serializers


class BaseSessionCommandSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    input = serializers.CharField(max_length=128)
    output = serializers.CharField(max_length=1024, allow_blank=True)
    session = serializers.CharField(max_length=36)
    org_id = serializers.CharField(max_length=36, required=False, default='', allow_null=True, allow_blank=True)
    timestamp = serializers.IntegerField()


class SessionCommandSerializer(BaseSessionCommandSerializer):
    """使用这个类作为基础Command Log Serializer类, 用来序列化"""
    user = serializers.CharField(max_length=64)
    asset = serializers.CharField(max_length=128)
    system_user = serializers.CharField(max_length=64)


class DatabaseSessionCommandSerializer(BaseSessionCommandSerializer):
    user_id = serializers.CharField(max_length=36)
    database = serializers.CharField(max_length=128)
    database_id = serializers.CharField(max_length=36)
    db_host = serializers.CharField(max_length=128)
    db_name = serializers.CharField(max_length=128)
    db_user = serializers.CharField(max_length=32)
