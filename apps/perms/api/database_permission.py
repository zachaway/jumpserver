#  coding: utf-8
#


from rest_framework import viewsets, generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import Response

from common.permissions import IsOrgAdmin

from ..models import DatabasePermission
from ..serializers import (
    DatabasePermissionSerializer,
    DatabasePermissionUpdateUserSerializer,
    DatabasePermissionUpdateDatabaseSerializer,
)


__all__ = [
    'DatabasePermissionViewSet',
    'DatabasePermissionRemoveUserApi', 'DatabasePermissionAddUserApi',
    'DatabasePermissionRemoveDatabaseApi', 'DatabasePermissionAddDatabaseApi',
]


class DatabasePermissionViewSet(viewsets.ModelViewSet):
    filter_fields = ('name', )
    search_fields = filter_fields
    queryset = DatabasePermission.objects.all()
    serializer_class = DatabasePermissionSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsOrgAdmin,)


class DatabasePermissionAddUserApi(generics.RetrieveUpdateAPIView):
    permission_classes = (IsOrgAdmin,)
    serializer_class = DatabasePermissionUpdateUserSerializer
    queryset = DatabasePermission.objects.all()

    def update(self, request, *args, **kwargs):
        perm = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            users = serializer.validated_data.get('users')
            if users:
                perm.users.add(*tuple(users))
            return Response({"msg": "ok"})
        else:
            return Response({"error": serializer.errors})


class DatabasePermissionRemoveUserApi(generics.RetrieveUpdateAPIView):
    permission_classes = (IsOrgAdmin,)
    serializer_class = DatabasePermissionUpdateUserSerializer
    queryset = DatabasePermission.objects.all()

    def update(self, request, *args, **kwargs):
        perm = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            users = serializer.validated_data.get('users')
            if users:
                perm.users.remove(*tuple(users))
            return Response({"msg": "ok"})
        else:
            return Response({"error": serializer.errors})


class DatabasePermissionAddDatabaseApi(generics.RetrieveUpdateAPIView):
    permission_classes = (IsOrgAdmin,)
    serializer_class = DatabasePermissionUpdateDatabaseSerializer
    queryset = DatabasePermission.objects.all()

    def update(self, request, *args, **kwargs):
        perm = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            databases = serializer.validated_data.get('databases')
            if databases:
                perm.databases.add(*tuple(databases))
            return Response({"msg": "ok"})
        else:
            return Response({"error": serializer.errors})


class DatabasePermissionRemoveDatabaseApi(generics.RetrieveUpdateAPIView):
    permission_classes = (IsOrgAdmin,)
    serializer_class = DatabasePermissionUpdateDatabaseSerializer
    queryset = DatabasePermission.objects.all()

    def update(self, request, *args, **kwargs):
        perm = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            databases = serializer.validated_data.get('databases')
            if databases:
                perm.databases.remove(*tuple(databases))
            return Response({"msg": "ok"})
        else:
            return Response({"error": serializer.errors})



