#coding:utf8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from teachmanager.models import *
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import requests
import jinja2
import markdown
from webapp.models import *
from django.contrib.auth.decorators import permission_required
from Publicapi.dockerapi.Manager import Dockerapi
from dockermanager.models import *
from webapp.Extends import PageList
from django.db.models import Q
from django.http import JsonResponse
from django.forms.models import model_to_dict

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
# Create your views here.

@login_required()
@csrf_exempt
@permission_required('teachmanager.add_experinfo',raise_exception=True) 
def experEdit(request):
    usersession = request.session.get('user_id')
    user_name = request.session.get('user_name')
    user=Suser.objects.filter(id=usersession)
    for i in user:
        creator = i.name
    if request.method == 'POST':
        try:
            experid = request.POST.get('experId')
        except:
            experid = None

        name = request.POST.get('name')
        introduction = request.POST.get('introduction')
        duration = request.POST.get('duration') 
        parent_id = request.POST.get('parent_id')
        detail = request.POST.get('detail')

        extensions = ['extra', 'smarty','markdown.extensions.codehilite','mdx_math']
        html = markdown.markdown(detail, output_format='html5', extensions=extensions)
        # doc = jinja2.Template(TEMPLATE).render(content=html)
        reserved1 = html
        parent_name=Sysinfo.objects.filter(sysid=parent_id)
        for i in parent_name:
            parent_name = i.name
        udict = {"name":name,"introduction":introduction,"duration":duration,"parent_id":parent_id,"detail":detail,"creator":creator,"reserved1":reserved1,"reserved2":parent_name}

        if experid:
            Experinfo.objects.filter(experid=experid).update(**udict)
            res ={"msg":"修改成功！","erro":0}
        else:
            Experinfo.objects.create(**udict)
            res ={"msg":"创建成功！","erro":0}
        return HttpResponse(json.dumps(res),content_type="application/json")
    else:
        res2=getsys()
        module = getmodule()
        option=Sysinfo.objects.filter(parent_id=-1).values("sysid","name")
        option = list(option)
        option =json.dumps(option,ensure_ascii=False)
        ret={'usersession':usersession,'option':option,'Sysinfo':res2,'module':module}
        return render_to_response('teachmanager/exper_info.html',ret,context_instance=RequestContext(request))


@login_required()
@csrf_exempt
@permission_required('teachmanager.view_experinfo',raise_exception=True) 
def experList(request,page):
    usersession = request.session.get('user_id')
    user_name = request.session.get('user_name')
    if request.method == 'GET':
        experinfo=Experinfo.objects.filter(is_delete = '0')
        (page,start,end,per_item)=PageList.PageCount(page)
        count = Experinfo.objects.filter(is_delete = '0').count()
        result = Experinfo.objects.filter(is_delete = '0').order_by('-experid')[start:end]
        url = "/teach/experlist"
        if count%per_item == 0:
            all_pages_count = count/per_item
        else:
            all_pages_count = count/per_item+1
        page=PageList.Page(page, url, all_pages_count)
        module = getmodule()
        option=Sysinfo.objects.filter(parent_id=-1).values("sysid","name")
        option = list(option)
        option =json.dumps(option,ensure_ascii=False)
        ret = {
               'count': count,
               'experinfo':result,
               'page': page,
               'usersession':usersession,
               'option':option,
               'module':module
               }
        return render(request,'teachmanager/exper_info_list.html',ret)
    else:
        searchdata = request.POST.get('search')
        #分页代码
        (page,start,end,per_item)=PageList.PageCount(page)
        experinfo=Experinfo.objects.filter(is_delete = '0')
        count=experinfo.filter(Q(duration=searchdata) |Q(reserved2__icontains=searchdata) |
                                       Q(creator__icontains=searchdata) | Q(name__icontains=searchdata)).count()

        result=experinfo.filter(Q(duration=searchdata) |Q(reserved2__icontains=searchdata) |
                                            Q(creator__icontains=searchdata) | Q(name__icontains=searchdata)).order_by('-experid')[start:end]
        url = "/teach/experlist"
        if count%per_item == 0:
            all_pages_count = count/per_item
        else:
            all_pages_count = count/per_item+1
        page=PageList.Page(page, url, all_pages_count)

        ret = {'experinfo': result,
               'count': count,
               'page': page,
               'usersession':usersession}
        return render(request,'teachmanager/exper_info_list.html',ret)

@login_required()
@csrf_exempt
@permission_required('teachmanager.delete_experinfo',raise_exception=True) 
def experDelete(request):
    usersession = request.session.get('user_id')
    user_name = request.session.get('user_name')
    if request.method == 'POST':
        experid = request.POST.get('id')
        crman = Experinfo.objects.filter(experid = experid).values('creator')
        for i in crman:
            crman = i['creator']
        user=Suser.objects.filter(id=usersession)
        for i in user:
            creator = i.name
        if creator == crman:     
            Experinfo.objects.filter(experid = experid).update(is_delete=True)
            res ={"msg":"删除成功"}
        else:
            res ={"msg":"不能删除他人的实验课程"}
        return HttpResponse(json.dumps(res),content_type="application/json")

@login_required()
@csrf_exempt
@permission_required('teachmanager.do_experiment',raise_exception=True) 
def experDetail(request):
    usersession = request.session.get('user_id')
    user_name = request.session.get('user_name')
    if request.method == 'GET':
        experid = request.GET.get('id')
        moduleid = request.GET.get('module')
        experdetail=Experinfo.objects.filter(experid=experid).values("reserved1")
        try:
            imageinfo=Sysinfo.objects.filter(sysid=moduleid).values("imagehost","repository","index_port")
            imageinfo = list(imageinfo)
            index_port = imageinfo[0]['index_port']
            imagehost = imageinfo[0]['imagehost']
            repository = imageinfo[0]['repository'].split(':')[0]
            dockerinfo=DockerHost.objects.filter(hostip=imagehost).values("hostip","port")
            docker_port = dockerinfo[0]['port']
            container_port = int(index_port)+int(usersession)
            Container_name=repository+'-'+str(usersession)      
            docker_Instance=Dockerapi(imagehost,docker_port)
            start=docker_Instance.StartContainer(Container_name)
            url = "http://"+imagehost+':'+str(container_port)
            ret={'usersession':usersession,'experdetail':experdetail,'url':url}
            return render(request,'teachmanager/exper_info_detail.html',ret)
        except:
            ret={'usersession':usersession,'experdetail':experdetail}
            return render(request,'teachmanager/exper_info_detail.html',ret)

    else:
        experid = request.POST.get('id')
        experinfo=Experinfo.objects.filter(experid=experid).values("experid","name","introduction","duration","parent_id","detail")
        experinfo = list(experinfo)
        ret={'experinfo':experinfo}
        return HttpResponse(json.dumps(ret),content_type="application/json")

@login_required()
@csrf_exempt
@permission_required('teachmanager.change_experinfo',raise_exception=True) 
def experchange(request):
    usersession = request.session.get('user_id')
    user_name = request.session.get('user_name')
    if request.method == 'GET':
        experid = request.GET.get('id')
        experinfo=Experinfo.objects.filter(experid=experid)
        ret={'usersession':usersession,'experinfo':experinfo}
        return render_to_response('teachmanager/exper_info.html',ret,context_instance=RequestContext(request))
    else:
        experid = request.POST.get('id')
        crman = Experinfo.objects.filter(experid = experid).values('creator')
        for i in crman:
            crman = i['creator']
        user=Suser.objects.filter(id=usersession)
        for i in user:
            creator = i.name
        if creator == crman:       
            experinfo=Experinfo.objects.filter(experid=experid).values("experid","name","introduction","duration","parent_id","detail")
            experinfo = list(experinfo)
            ret={'experinfo':experinfo,"msg":"success"}
        else:
            ret ={"msg":"不能编辑他人的实验课程"}
        return HttpResponse(json.dumps(ret),content_type="application/json")

@login_required()
@csrf_exempt
@permission_required('teachmanager.view_sysinfo',raise_exception=True) 
def sysList(request):
    usersession = request.session.get('user_id')
    user_name = request.session.get('user_name')
    if request.method == 'POST':
        usersession = request.session.get('user_id')
        try:
            sysid = request.POST.get['sysid']
        except:
            sysid = None
        name = request.POST.get('name')
        description = request.POST.get('description')
        parent_id = request.POST.get('parent_id')
        try:
            imagehost = request.POST.get('imagehost')
            repository = request.POST.get('repository')
            index_port = request.POST.get('port')
            udict = {"name":name,"description":description,"parent_id":parent_id,"imagehost":imagehost,"repository":repository,"index_port":index_port}
        except:
             udict = {"name":name,"description":description,"parent_id":parent_id}
        if sysid:
            Sysinfo.objects.filter(sysid=sysid).update(**udict)
            res ={"msg":"修改成功！","erro":0}
        else:
            Sysinfo.objects.create(**udict)
            res ={"msg":"创建成功！","erro":0}
        return HttpResponse(json.dumps(res),content_type="application/json")
    else:
        res2=getmodule()
        module = getmodule()
        option=Sysinfo.objects.filter(parent_id=-1,is_delete = '0').values("sysid","name")
        option = list(option)
        option =json.dumps(option,ensure_ascii=False)
        Image=Dockerimage.objects.values("imagehost","repository")
        Image = list(Image)
        Image =json.dumps(Image,ensure_ascii=False)
        ret={'usersession':usersession,'Sysinfo':res2,'option':option,'module':module,'Image':Image}
        return render_to_response('teachmanager/sys_info.html',ret,context_instance=RequestContext(request))


@login_required()
@csrf_exempt
@permission_required('teachmanager.change_sysinfo',raise_exception=True) 
def syschange(request):
    usersession = request.session.get('user_id')
    user_name = request.session.get('user_name')
    if request.method == 'GET':
        sysid = request.GET.get('categoryId')
        sysinfo=Sysinfo.objects.filter(sysid=sysid).values("name","description","parent_id","imagehost","index_port","repository")
        sysinfo = list(sysinfo)
        ret={'usersession':usersession,'sysinfo':sysinfo}
        return HttpResponse(json.dumps(ret),content_type="application/json")
    if request.method == 'POST':
        usersession = request.session.get('user_id')
        sysid = request.POST.get('sysid')
        name = request.POST.get('name')
        description = request.POST.get('description')
        parent_id = request.POST.get('parent_id')
        try:
            imagehost = request.POST.get('imagehost')
            repository = request.POST.get('repository')
            index_port = request.POST.get('port')
            udict = {"name":name,"description":description,"parent_id":parent_id,"imagehost":imagehost,"repository":repository,"index_port":index_port}
        except:
             udict = {"name":name,"description":description,"parent_id":parent_id}

        Sysinfo.objects.filter(sysid=sysid).update(**udict)
        ret ={"msg":"修改成功","erro":0}
        return render_to_response('teachmanager/sys_info.html',ret,context_instance=RequestContext(request))


@login_required()
@csrf_exempt
@permission_required('teachmanager.delete_sysinfo',raise_exception=True) 
def sys_del(request):
    if request.method == 'POST':
        sysid = request.POST.get('sysid')
        Sysinfo.objects.filter(sysid = sysid).update(is_delete=True)
        res ={"msg":"删除成功"}
        return HttpResponse(json.dumps(res),content_type="application/json")


@login_required()
@csrf_exempt
def classlist2(request,page):
    usersession = request.session.get('user_id')
    user_name = request.session.get('user_name')
    if request.method == 'GET':
        try:
            moduleid = request.GET.get('id')
        except:
            moduleid = None  
        if moduleid:
            (page,start,end,per_item)=PageList.PageCount(page)
            experinfo=Experinfo.objects.filter(is_delete = '0',parent_id = moduleid)
            count=experinfo.count()
            result=experinfo.order_by('-experid')[start:end]
            url = "/teach/experlist"
            if count%per_item == 0:
                all_pages_count = count/per_item
            else:
                all_pages_count = count/per_item+1
            page=PageList.Page(page, url, all_pages_count)
            result = map(model_to_dict,result) #把对象转换成dict形式 key-value ，之后就可以被序列化了
            ret = {'experinfo': result,
               'count': count,
               'page': page,
               'usersession':usersession}
        else:
            ret={'msg':moduleid}
            pass      
        return JsonResponse(ret)


def getsys():
    sysinfo=Sysinfo.objects.filter(is_delete = '0')
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
    dic1 = {}
    for i,j in res.items():
        dic1 = {"text":i.split(":")[1]}
        if j != {}:
            dic1["nodes"] =  []  
            dict2 = {}
            for m,n in j.items():
                dict2["text"] = m.split(":")[1]
                if n != {}:
                    dict2["nodes"] = []
                    for h in n:
                        dict2["nodes"].append({"text":h.split(":")[1]})
                dic1["nodes"].append({"text":dict2["text"]})
        res2.append(dic1) 
    res2 =json.dumps(res2,ensure_ascii=False)
    return res2
def getmodule():
    sysinfo=Sysinfo.objects.filter(is_delete = '0')
    res = {}
    for it in sysinfo:
        if it.parent_id == -1:
            res[str(it.sysid)+":"+it.name]={}
    for it in sysinfo:
        if it.parent_id != -1:
            flag1,flag2 = 0,0
            for i,j in res.items():
                if i.split(":")[0] == str(it.parent_id):
                    res[i][str(it.sysid)+":"+it.name] = {}
                    flag1 = 1
                    break
            if flag1 == 1:
                continue
            # for i,j in res.items():
            #     for m,n in j.items():
            #         if m.split(":")[0] == str(it.parent_id ):
            #             res[i][m][str(it.sysid)+":"+it.name] = {}
            #             flag2 = 1
            #             break
            #     if flag2 == 1:
            #         break
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





