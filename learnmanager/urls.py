#coding:utf8
from django.conf.urls import url
from views import learnlist,classlist,pptlist,bglist

urlpatterns = [
    url(r'learn/$',learnlist,name='learnlist'),
    url(r'class/$',classlist,name='classlist'),
    url(r'pptlist/$',pptlist,name='pptlist'),
    url(r'bglist/$',bglist,name='bglist'),

]
