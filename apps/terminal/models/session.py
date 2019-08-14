# coding: utf-8
#

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.cache import cache

from .base import BaseSession


__all__ = ['Session', 'DatabaseSession']


class Session(BaseSession):
    """
    AssetSession
    """
    PROTOCOL_CHOICES = (
        ('ssh', 'ssh'),
        ('rdp', 'rdp'),
        ('vnc', 'vnc')
    )
    asset = models.CharField(max_length=1024, verbose_name=_("Asset"))
    system_user = models.CharField(max_length=128, verbose_name=_("System user"))
    protocol = models.CharField(choices=PROTOCOL_CHOICES, default='ssh', max_length=8)

    _DATE_START_FIRST_HAS_REPLAY_RDP_SESSION = None

    @property
    def _date_start_first_has_replay_rdp_session(self):
        if self.__class__._DATE_START_FIRST_HAS_REPLAY_RDP_SESSION is None:
            instance = self.__class__.objects.filter(
                protocol='rdp', has_replay=True
            ).order_by('date_start').first()
            if not instance:
                date_start = timezone.now() - timezone.timedelta(days=365)
            else:
                date_start = instance.date_start
            self.__class__._DATE_START_FIRST_HAS_REPLAY_RDP_SESSION = date_start
        return self.__class__._DATE_START_FIRST_HAS_REPLAY_RDP_SESSION

    def can_replay(self):
        if self.has_replay:
            return True
        if self.date_start < self._date_start_first_has_replay_rdp_session:
            return True
        return False

    def is_active(self):
        if self.protocol in ['ssh', 'telnet']:
            key = self.ACTIVE_CACHE_KEY_PREFIX.format(self.id)
            return bool(cache.get(key))
        return True

    class Meta:
        db_table = "terminal_session"
        ordering = ["-date_start"]

    def __str__(self):
        return "{0.id} of {0.user} to {0.asset}".format(self)


class DatabaseSession(BaseSession):
    user_id = models.CharField(max_length=36, db_index=True, verbose_name=_("User ID"))
    database = models.CharField(max_length=128, verbose_name=_('Database'))
    database_id = models.CharField(max_length=36, db_index=True, verbose_name=_("Database ID"))
    db_host = models.CharField(max_length=128, verbose_name=_('Database host'))
    db_name = models.CharField(max_length=128, blank=True, null=True, verbose_name=_('Database name'))
    db_user = models.CharField(max_length=32, blank=True, null=True, verbose_name=_('Database user'))

    def can_replay(self):
        return self.has_replay

    class Meta:
        db_table = "terminal_database_session"
        ordering = ["-date_start"]
