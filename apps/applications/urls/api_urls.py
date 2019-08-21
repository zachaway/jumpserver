# coding:utf-8
#

from django.urls import path, re_path
from rest_framework_bulk.routes import BulkRouter

from common import api as capi
from .. import api

app_name = 'applications'

router = BulkRouter()
router.register(r'remote-apps', api.RemoteAppViewSet, 'remote-app')
router.register(r'databases', api.DatabaseViewSet, 'database')

urlpatterns = [
    path('remote-apps/<uuid:pk>/connection-info/', api.RemoteAppConnectionInfoApi.as_view(), name='remote-app-connection-info'),
    path('databases/<uuid:pk>/auth-info/', api.DatabaseAuthInfoApi.as_view(), name='database-auth-info')
]
old_version_urlpatterns = [
    re_path('(?P<resource>remote-app)|database/.*', capi.redirect_plural_name_api)
]

urlpatterns += router.urls + old_version_urlpatterns
