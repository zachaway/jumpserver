# coding: utf-8
#

from django.utils.translation import ugettext as _
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from common.permissions import PermissionsMixin, IsOrgAdmin, IsValidUser
from common.const import create_success_msg, update_success_msg

from .. import forms
from ..models import Database

__all__ = [
    'DatabaseListView', 'DatabaseCreateView', 'DatabaseUpdateView',
    'DatabaseDetailView', 'UserDatabaseListView'
]


class DatabaseListView(PermissionsMixin, TemplateView):
    template_name = 'applications/database_list.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Applications'),
            'action': _('Database list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class DatabaseCreateView(PermissionsMixin, SuccessMessageMixin, CreateView):
    template_name = 'applications/database_create_update.html'
    permission_classes = [IsOrgAdmin]
    model = Database
    form_class = forms.DatabaseCreateUpdateForm
    success_url = reverse_lazy('applications:database-list')

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Applications'),
            'action': _('Create Database'),
            'type': 'create',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get_success_message(self, cleaned_data):
        return create_success_msg % ({'name': cleaned_data['name']})


class DatabaseUpdateView(PermissionsMixin, SuccessMessageMixin, UpdateView):
    template_name = 'applications/database_create_update.html'
    permission_classes = [IsOrgAdmin]
    model = Database
    form_class = forms.DatabaseCreateUpdateForm
    success_url = reverse_lazy('applications:database-list')

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Applications'),
            'action': _('Update Database'),
            'type': 'update',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get_success_message(self, cleaned_data):
        return update_success_msg % ({'name': cleaned_data['name']})


class DatabaseDetailView(PermissionsMixin, DetailView):
    template_name = 'applications/database_detail.html'
    permission_classes = [IsOrgAdmin]
    model = Database
    context_object_name = 'database'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Applications'),
            'action': _('Database detail'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserDatabaseListView(PermissionsMixin, TemplateView):
    template_name = 'applications/user_database_list.html'
    permission_classes = [IsValidUser]

    def get_context_data(self, **kwargs):
        context = {
            'action': _('My database'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
