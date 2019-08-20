# coding: utf-8
#

from django.db.models import Q
from orgs.utils import set_to_root_org

from ..models import DatabasePermission

__all__ = ['DatabasePermissionUtil']


def get_user_database_permissions(user, include_group=True):
    if include_group:
        groups = user.groups.all()
        arg = Q(users=user) | Q(user_groups__in=groups)
    else:
        arg = Q(users=user)
    return DatabasePermission.objects.all().valid().filter(arg)


def get_user_group_database_permissions(user_group):
    return DatabasePermission.objects.all().valid().filter(user_groups=user_group)


class DatabasePermissionUtil:
    get_permissions_map = {
        'User': get_user_database_permissions,
        'UserGroup': get_user_group_database_permissions
    }

    def __init__(self, obj):
        self.object = obj
        self.change_org_if_need()

    @staticmethod
    def change_org_if_need():
        set_to_root_org()

    @property
    def permissions(self):
        obj_class = self.object.__class__.__name__
        func = self.get_permissions_map.get(obj_class)
        _permissions = func(self.object)
        return _permissions

    def get_databases(self):
        databases = set()
        for perm in self.permissions:
            databases.update(list(perm.databases.all()))
        return databases
