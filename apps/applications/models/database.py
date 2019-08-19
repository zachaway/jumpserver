# coding: utf-8
#

import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _

from orgs.mixins import OrgModelMixin
from common.validators import alphanumeric
from common import fields

__all__ = ["Database"]


class Database(OrgModelMixin):
    LOGIN_AUTO = 'auto'
    LOGIN_MANUAL = 'manual'
    LOGIN_MODE_CHOICES = (
        (LOGIN_AUTO, _("Automatic login")),
        (LOGIN_MANUAL, _("Manually login"))
    )

    TYPE_MYSQL = 'mysql'
    TYPE_CHOICES = (
        (TYPE_MYSQL, _('MySQL')),
    )

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    login_mode = models.CharField(
        choices=LOGIN_MODE_CHOICES, default=LOGIN_AUTO, max_length=10,
        verbose_name=_('Login mode')
    )
    type = models.CharField(
        choices=TYPE_CHOICES, default=TYPE_MYSQL, max_length=10,
        verbose_name=_('Type')
    )
    host = models.CharField(max_length=128, verbose_name=_('Host'))
    port = models.IntegerField(default=3306, verbose_name=_('Port'))
    user = models.CharField(
        max_length=32, blank=True, null=True, validators=[alphanumeric],
        verbose_name=_('User')
    )
    password = fields.EncryptCharField(
        max_length=256, blank=True, null=True, verbose_name=_('Password')
    )
    database = models.CharField(
        max_length=128, blank=True, null=True, verbose_name=_('Database')
    )
    comment = models.TextField(blank=True, verbose_name=_('Comment'))
    created_by = models.CharField(
        max_length=128, null=True, verbose_name=_('Created by')
    )
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date Created')
    )
    date_updated = models.DateTimeField(
        auto_now=True, verbose_name=_('Date updated')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Database')
        unique_together = [('org_id', 'name')]
        ordering = ('name',)
