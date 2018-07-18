#coding:utf8
from django.conf.urls import url

from views import experEdit,experList,experDetail,sysList,experchange,sys_del,syschange,experDelete,classlist2

urlpatterns = [
    url(r'exper/$',experEdit,name='experEdit'),
    url(r'experlist/(\d+)$',experList,name='experList'),
    url(r'experchange/$',experchange,name='experchange'),
    url(r'experdelete/$',experDelete,name='experDelete'),
    url(r'experdetail/$',experDetail,name='experDetail'),
    url(r'syslist/$',sysList,name='sysList'),
    url(r'sys_del/$',sys_del,name='sys_del'),
    url(r'syschange/$',syschange,name='syschange'),
    url(r'classlist2/(\d+)$',classlist2,name='classlist2'),


]
