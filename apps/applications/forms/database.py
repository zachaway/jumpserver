# coding: utf-8
#

from django import forms
from django.utils.translation import ugettext as _

from orgs.mixins import OrgModelForm

from ..models import Database


__all__ = ['DatabaseCreateUpdateForm']


class DatabaseCreateUpdateForm(OrgModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput, max_length=128,
        strip=True, required=False, label=_("Password"),
    )

    class Meta:
        model = Database
        fields = [
            'name', 'login_mode', 'type', 'host', 'port', 'user', 'password',
            'database', 'comment'
        ]
        help_texts = {
            'login_mode': _('If you choose manual login mode, you do not '
                            'need to fill in the user and password.'),
        }
