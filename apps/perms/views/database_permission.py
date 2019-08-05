# coding: utf-8
#

from django.utils.translation import ugettext as _
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, CreateView, UpdateView, DetailView, ListView
)
from django.views.generic.edit import SingleObjectMixin
from django.conf import settings

from common.permissions import PermissionsMixin, IsOrgAdmin
from orgs.utils import current_org

from ..hands import Database, UserGroup
from ..models import DatabasePermission
from ..forms import DatabasePermissionCreateUpdateForm


__all__ = [
    'DatabasePermissionListView', 'DatabasePermissionCreateView',
    'DatabasePermissionUpdateView', 'DatabasePermissionDetailView',
    'DatabasePermissionUserView', 'DatabasePermissionDatabaseView'
]


class DatabasePermissionListView(PermissionsMixin, TemplateView):
    template_name = 'perms/database_permission_list.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Perms'),
            'action': _('Database permission list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class DatabasePermissionCreateView(PermissionsMixin, CreateView):
    template_name = 'perms/database_permission_create_update.html'
    model = DatabasePermission
    form_class = DatabasePermissionCreateUpdateForm
    success_url = reverse_lazy('perms:database-permission-list')
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Perms'),
            'action': _('Create database permission'),
            'type': 'create'
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class DatabasePermissionUpdateView(PermissionsMixin, UpdateView):
    template_name = 'perms/database_permission_create_update.html'
    model = DatabasePermission
    form_class = DatabasePermissionCreateUpdateForm
    success_url = reverse_lazy('perms:database-permission-list')
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Perms'),
            'action': _('Update database permission'),
            'type': 'update'
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class DatabasePermissionDetailView(PermissionsMixin, DetailView):
    template_name = 'perms/database_permission_detail.html'
    model = DatabasePermission
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Perms'),
            'action': _('Database permission detail'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class DatabasePermissionUserView(PermissionsMixin,
                                 SingleObjectMixin,
                                 ListView):
    template_name = 'perms/database_permission_user.html'
    context_object_name = 'database_permission'
    paginate_by = settings.DISPLAY_PER_PAGE
    object = None
    permission_classes = [IsOrgAdmin]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=DatabasePermission.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = list(self.object.get_all_users())
        return queryset

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Perms'),
            'action': _('Database permission user list'),
            'users_remain': current_org.get_org_users().exclude(
                databasepermission=self.object
            ),
            'user_groups_remain': UserGroup.objects.exclude(
                databasepermission=self.object
            )
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class DatabasePermissionDatabaseView(PermissionsMixin,
                                     SingleObjectMixin,
                                     ListView):
    template_name = 'perms/database_permission_database.html'
    context_object_name = 'database_permission'
    paginate_by = settings.DISPLAY_PER_PAGE
    object = None
    permission_classes = [IsOrgAdmin]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(
            queryset=DatabasePermission.objects.all()
        )
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = list(self.object.get_all_databases())
        return queryset

    def get_context_data(self, **kwargs):
        database_granted = self.get_queryset()
        database_remain = Database.objects.exclude(
            id__in=[a.id for a in database_granted])
        context = {
            'app': _('Perms'),
            'action': _('Database permission database list'),
            'database_remain': database_remain
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
