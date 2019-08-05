#  coding: utf-8
#

from django.utils.translation import ugettext as _
from django import forms
from orgs.mixins import OrgModelForm
from orgs.utils import current_org

from ..models import DatabasePermission


__all__ = [
    'DatabasePermissionCreateUpdateForm',
]


class DatabasePermissionCreateUpdateForm(OrgModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users_field = self.fields.get('users')
        if hasattr(users_field, 'queryset'):
            users_field.queryset = current_org.get_org_users()

    class Meta:
        model = DatabasePermission
        exclude = (
            'id', 'date_created', 'created_by', 'org_id'
        )
        widgets = {
            'users': forms.SelectMultiple(
                attrs={'class': 'select2', 'data-placeholder': _('User')}
            ),
            'user_groups': forms.SelectMultiple(
                attrs={'class': 'select2', 'data-placeholder': _('User group')}
            ),
            'databases': forms.SelectMultiple(
                attrs={'class': 'select2', 'data-placeholder': _('Database')}
            )
        }
