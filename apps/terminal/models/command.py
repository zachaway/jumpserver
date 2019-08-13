# coding: utf-8
#
from __future__ import unicode_literals

from ..backends.command.models import (
    AbstractSessionCommand, AbstractDatabaseSessionCommand
)


__all__ = ['Command', 'DatabaseCommand']


class Command(AbstractSessionCommand):

    class Meta:
        db_table = "terminal_command"
        ordering = ('-timestamp',)


class DatabaseCommand(AbstractDatabaseSessionCommand):

    class Meta:
        db_table = "terminal_database_command"
        ordering = ('-timestamp', )
