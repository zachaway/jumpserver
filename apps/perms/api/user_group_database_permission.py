# coding: utf-8
#


from rest_framework.generics import (
    ListAPIView, get_object_or_404
)

from common.permissions import IsOrgAdminOrAppUser

from ..utils import DatabasePermissionUtil
from ..hands import UserGroup, DatabaseSerializer

__all__ = [
    'UserGroupGrantedDatabasesApi'
]


class UserGroupGrantedDatabasesApi(ListAPIView):
    permission_classes = (IsOrgAdminOrAppUser,)
    serializer_class = DatabaseSerializer

    def get_queryset(self):
        queryset = []
        user_group_id = self.kwargs.get('pk')
        if not user_group_id:
            return queryset
        user_group = get_object_or_404(UserGroup, id=user_group_id)
        util = DatabasePermissionUtil(user_group)
        queryset = util.get_databases()
        return queryset
