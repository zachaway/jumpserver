# coding: utf-8
#

from __future__ import unicode_literals

import os
import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.files.storage import default_storage
from django.core.cache import cache

from ..backends import get_multi_command_storage
from orgs.mixins import OrgModelMixin
from .terminal import Terminal


__all__ = ['BaseSession']


class BaseSession(OrgModelMixin):
    LOGIN_FROM_CHOICES = (
        ('ST', 'SSH Terminal'),
        ('WT', 'Web Terminal'),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.CharField(max_length=128, verbose_name=_("User"))
    login_from = models.CharField(max_length=2, choices=LOGIN_FROM_CHOICES, default="ST")
    remote_addr = models.CharField(max_length=15, verbose_name=_("Remote addr"), blank=True, null=True)
    is_finished = models.BooleanField(default=False)
    has_replay = models.BooleanField(default=False, verbose_name=_("Replay"))
    has_command = models.BooleanField(default=False, verbose_name=_("Command"))
    terminal = models.ForeignKey(Terminal, null=True, on_delete=models.SET_NULL)
    date_last_active = models.DateTimeField(verbose_name=_("Date last active"), default=timezone.now)
    date_start = models.DateTimeField(verbose_name=_("Date start"), db_index=True, default=timezone.now)
    date_end = models.DateTimeField(verbose_name=_("Date end"), null=True)

    upload_to = 'replay'
    ACTIVE_CACHE_KEY_PREFIX = 'SESSION_ACTIVE_{}'

    def get_rel_replay_path(self, version=2):
        """
        获取session日志的文件路径
        :param version: 原来后缀是 .gz，为了统一新版本改为 .replay.gz
        :return:
        """
        suffix = '.replay.gz'
        if version == 1:
            suffix = '.gz'
        date = self.date_start.strftime('%Y-%m-%d')
        return os.path.join(date, str(self.id) + suffix)

    def get_local_path(self, version=2):
        rel_path = self.get_rel_replay_path(version=version)
        if version == 2:
            local_path = os.path.join(self.upload_to, rel_path)
        else:
            local_path = rel_path
        return local_path

    def save_to_storage(self, f):
        local_path = self.get_local_path()
        try:
            name = default_storage.save(local_path, f)
            return name, None
        except OSError as e:
            return None, e

    @classmethod
    def set_sessions_active(cls, sessions_id):
        data = {cls.ACTIVE_CACHE_KEY_PREFIX.format(i): i for i in sessions_id}
        cache.set_many(data, timeout=5*60)

    @classmethod
    def get_active_sessions(cls):
        return cls.objects.filter(is_finished=False)

    def is_active(self):
        key = self.ACTIVE_CACHE_KEY_PREFIX.format(self.id)
        return bool(cache.get(key))

    @property
    def command_amount(self):
        command_store = get_multi_command_storage()
        return command_store.count(session=str(self.id))

    @property
    def login_from_display(self):
        return self.get_login_from_display()

    class Meta:
        abstract = True


