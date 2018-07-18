from django.conf.urls import url

from saltadmin.views import (KeyList,Minion_Status,SoftInstall,JobList,RemoteCmd,SaltMasterList,
                              SaltMinionGrains,CmdResult,jobdetail,DeployResult,SaltMasterDelete,
                              SalMasterChange
                             )

urlpatterns = [
    url(r'keylist/', KeyList, name='KeyList'),
    url(r'minion/status/',Minion_Status,name='Minion_Status'),
    url(r'minion/softinstall/',SoftInstall,name='SoftInstall'),
    url(r'job/list/(?P<page>\d+)',JobList,name='JobList'),
    url(r'cmd/$',RemoteCmd,name='RemoteCmd'),
    url(r'master/$',SaltMasterList,name='SaltMasterList'),
    url(r'master/delete/(?P<masterid>\d+)$',SaltMasterDelete,name='SaltMasterDelete'),
    url(r'master/change/(?P<masterid>\d+)$',SalMasterChange,name='SalMasterChange'),
    url(r'grains/$',SaltMinionGrains,name='SaltMinionGrains'),
    url(r'cmdresult/(?P<jid>\d+)$',CmdResult,name='CmdResult'),
    url(r'deployresult/(?P<jid>\d+)$',DeployResult,name='DeployResult'),
    url(r'job/detail/$',jobdetail,name='jobdetail'),
]
