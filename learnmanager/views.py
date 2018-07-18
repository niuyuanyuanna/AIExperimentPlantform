#coding:utf8

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from learnmanager.models import *
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from teachmanager.models import *
import json
import os
from Publicapi.dockerapi.Manager import Dockerapi
from dockermanager.models import *

from django.conf import settings as django_settings
# Create your views here.

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

@login_required()
@csrf_exempt
def learnlist(request):
    usersession = request.session.get('user_id')
    user_name = request.session.get('user_name')
    if request.method == 'GET':
     	module = getmodule()
        option=Sysinfo.objects.filter(parent_id=-1).values("sysid","name")
        option = list(option)
        option =json.dumps(option,ensure_ascii=False)
        ret={'usersession':usersession,'option':option,'module':module}
        return render_to_response('learnmanager/learnlist.html',ret,context_instance=RequestContext(request))
    else:
        return HttpResponse(content_type="application/json")

@login_required()
@csrf_exempt
def classlist(request):
    usersession = request.session.get('user_id')
    user_name = request.session.get('user_name')
    if request.method == 'GET':
        try:
            moduleid = request.GET.get('id')
        except:
            moduleid = None
        if moduleid:
            experinfo=Experinfo.objects.filter(is_delete = '0',parent_id = moduleid).values("experid","name")
            experinfo = list(experinfo)
            ret={'usersession':usersession,'experinfo':experinfo}
        else:
            ret={'msg':moduleid}
            pass
        return HttpResponse(json.dumps(ret,ensure_ascii=False),content_type="application/json")


@login_required()
@csrf_exempt
def pptlist(request):
    usersession = request.session.get('user_id')
    user_name = request.session.get('user_name')
    if request.method == 'GET':
        fi = file_name('/data/testSimpletourDevops/static/suit/ai-ppt')
        fi = json.dumps(fi,ensure_ascii=False)
        ret={'usersession':usersession,'file':fi}
        return render_to_response('learnmanager/pptlist.html',ret,context_instance=RequestContext(request))
    else:
       pass

@login_required()
@csrf_exempt
def bglist(request):
    usersession = request.session.get('user_id')
    user_name = request.session.get('user_name')
    if request.method == 'GET':
        fi = bg_name('/data/testSimpletourDevops/static/suit/bg-ppt')
        fi = json.dumps(fi,ensure_ascii=False)
        ret={'usersession':usersession,'file':fi}
        return render_to_response('learnmanager/bglist.html',ret,context_instance=RequestContext(request))
    else:
       pass
def bg_name(file_dir):   
    L=[]   
    dict1={}
    for root, dirs, files in os.walk(file_dir):
        for file in files:  
            if os.path.splitext(file)[1] == '.html':
                file = file.split('.')[0]
                dict1['name']=file
                dict1['html'] = django_settings.WEB_DOMAIN+'/static/bg-ppt/'+str(file)+'.html'
            L.append({'name':dict1['name'],'html':dict1['html']})
            L = sorted(L,key = lambda x:x['name'].split('-')[0], reverse=False) 
            
    return L

def file_name(file_dir):   
    L=[]   
    dict1={}
    for root, dirs, files in os.walk(file_dir):
        for file in files:  
            if os.path.splitext(file)[1] == '.html':
                file = file.split('.')[0]
                dict1['name']=file
                dict1['html'] = django_settings.WEB_DOMAIN+'/static/ai-ppt/'+str(file)+'.html'
            L.append({'name':dict1['name'],'html':dict1['html']})
            L = sorted(L,key = lambda x:x['name'].split('-')[0], reverse=False) 
            
    return L

def getmodule():
    sysinfo=Sysinfo.objects.all()
    res = {}
    for it in sysinfo:
        if it.parent_id == -1:
            res[str(it.sysid)+":"+it.name]={}
        else:
            flag1,flag2 = 0,0
            for i,j in res.items():
                if i.split(":")[0] == str(it.parent_id):
                    res[i][str(it.sysid)+":"+it.name] = {}
                    flag1 = 1
                    break
            if flag1 == 1:
                continue
            
            for i,j in res.items():
                for m,n in j.items():
                    if m.split(":")[0] == str(it.parent_id ):
                        res[i][m][str(it.sysid)+":"+it.name] = {}
                        flag2 = 1
                        break
                if flag2 == 1:
                    break
    res2 = []
    for i,j in res.items():
        dic1 = {"text":i.split(":")[1],"sysid":i.split(":")[0]}
        if j != {}:
            dic1["nodes"] =  []  
            dict2 = {}
            for m,n in j.items():
                dict2["text"] = m.split(":")[1]
                dict2["sysid"] = m.split(":")[0]
                if n != {}:
                    dict2["nodes"] = []
                    for h in n:
                        dict2["nodes"].append({"text":h.split(":")[1],"sysid":h.split(":")[0]})
                dic1["nodes"].append({"text":dict2["text"],"sysid":dict2["sysid"]})
        res2.append(dic1)   
    res2 =json.dumps(res2,ensure_ascii=False)
    return res2

