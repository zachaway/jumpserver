# coding: utf-8
# 
from __future__ import unicode_literals

import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.cache import cache

from users.models import User
from common.utils import (
    get_command_storage_setting, get_replay_storage_setting, get_validity_of_license
)


__all__ = ['Terminal']


class Terminal(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=32, verbose_name=_('Name'))
    remote_addr = models.CharField(max_length=128, blank=True, verbose_name=_('Remote Address'))
    ssh_port = models.IntegerField(verbose_name=_('SSH Port'), default=2222)
    http_port = models.IntegerField(verbose_name=_('HTTP Port'), default=5000)
    command_storage = models.CharField(max_length=128, verbose_name=_("Command storage"), default='default')
    replay_storage = models.CharField(max_length=128, verbose_name=_("Replay storage"), default='default')
    user = models.OneToOneField(User, related_name='terminal', verbose_name='Application User', null=True, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False, verbose_name='Is Accepted')
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, verbose_name=_('Comment'))
    STATUS_KEY_PREFIX = 'terminal_status_'

    @property
    def is_alive(self):
        key = self.STATUS_KEY_PREFIX + str(self.id)
        return bool(cache.get(key))

    @is_alive.setter
    def is_alive(self, value):
        key = self.STATUS_KEY_PREFIX + str(self.id)
        cache.set(key, value, 60)

    @property
    def is_active(self):
        if self.user and self.user.is_active:
            return True
        return False

    @is_active.setter
    def is_active(self, active):
        if self.user:
            self.user.is_active = active
            self.user.save()

    def get_command_storage_setting(self):
        storage_all = get_command_storage_setting()
        if self.command_storage in storage_all:
            storage = storage_all.get(self.command_storage)
        else:
            storage = storage_all.get('default')
        return {"TERMINAL_COMMAND_STORAGE": storage}

    def get_replay_storage_setting(self):
        storage_all = get_replay_storage_setting()
        if self.replay_storage in storage_all:
            storage = storage_all.get(self.replay_storage)
        else:
            storage = storage_all.get('default')
        return {"TERMINAL_REPLAY_STORAGE": storage}

    @property
    def config(self):
        configs = {}
        for k in dir(settings):
            if not k.startswith('TERMINAL'):
                continue
            configs[k] = getattr(settings, k)
        configs.update(self.get_command_storage_setting())
        configs.update(self.get_replay_storage_setting())
        configs.update({
            'SECURITY_MAX_IDLE_TIME': settings.SECURITY_MAX_IDLE_TIME,
            'LICENSE_VALID': get_validity_of_license(),
        })
        return configs

    @property
    def service_account(self):
        return self.user

    def create_app_user(self):
        random = uuid.uuid4().hex[:6]
        user, access_key = User.create_app_user(
            name="{}-{}".format(self.name, random), comment=self.comment
        )
        self.user = user
        self.save()
        return user, access_key

    def delete(self, using=None, keep_parents=False):
        if self.user:
            self.user.delete()
        self.user = None
        self.is_deleted = True
        self.save()
        return

    def __str__(self):
        status = "Active"
        if not self.is_accepted:
            status = "NotAccept"
        elif self.is_deleted:
            status = "Deleted"
        elif not self.is_active:
            status = "Disable"
        return '%s: %s' % (self.name, status)

    class Meta:
        ordering = ('is_accepted',)
        db_table = "terminal"
