# -*- coding: utf-8 -*-
#

from django.views.generic import ListView, TemplateView
from django.views.generic.edit import SingleObjectMixin
from django.utils.translation import ugettext as _

from common.permissions import PermissionsMixin, IsOrgAdmin, IsAuditor
from ..models import Session
from ..backends import get_multi_command_storage
from .base_session import BaseSessionListView


__all__ = [
    'SessionOnlineListView', 'SessionOfflineListView',
    'SessionDetailView',
]


class SessionListView(BaseSessionListView):
    model = Session
    template_name = 'terminal/asset_session_list.html'


class SessionOnlineListView(SessionListView):
    def get_context_data(self, **kwargs):
        context = {
            'app': _('Sessions'),
            'action': _('Session online list'),
            'type': 'online',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class SessionOfflineListView(SessionListView):
    def get_context_data(self, **kwargs):
        context = {
            'app': _('Sessions'),
            'action': _('Session offline'),
            'type': 'offline',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class SessionDetailView(SingleObjectMixin, PermissionsMixin, ListView):
    template_name = 'terminal/asset_session_detail.html'
    model = Session
    object = None
    permission_classes = [IsOrgAdmin | IsAuditor]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.model.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        command_store = get_multi_command_storage()
        return command_store.filter(session=self.object.id)

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Sessions'),
            'action': _('Session detail'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

