# coding: utf-8
# 

from django.views.generic import TemplateView
from django.utils import timezone

from common.permissions import PermissionsMixin, IsOrgAdmin, IsAuditor


__all__ = ['BaseSessionListView']


class BaseSessionListView(PermissionsMixin, TemplateView):
    model = None
    template_name = None
    date_from = date_to = None
    permission_classes = [IsOrgAdmin | IsAuditor]
    default_days_ago = 5

    def get_context_data(self, **kwargs):
        now = timezone.now()
        context = {
            'date_from': now - timezone.timedelta(days=self.default_days_ago),
            'date_to': now,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
