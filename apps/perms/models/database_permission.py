#  coding: utf-8
#

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import BasePermission

__all__ = [
    'DatabasePermission',
]


class DatabasePermission(BasePermission):
    databases = models.ManyToManyField(
        'applications.Database', related_name='granted_by_permissions',
        blank=True, verbose_name=_("Database")
    )

    class Meta:
        unique_together = [('org_id', 'name')]
        verbose_name = _('Database permission')
        ordering = ('name',)

    def get_all_databases(self):
        return set(self.databases.all())

