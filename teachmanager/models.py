#coding:utf8
from __future__ import unicode_literals

from django.db import models


class Sysinfo(models.Model):
    sysid = models.AutoField(primary_key=True,verbose_name=u'体系id')
    name = models.CharField(u'体系名', max_length=20)
    description = models.CharField(u'体系描述', max_length=200,blank=True)
    parent_id = models.IntegerField(u'父类id')
    level= models.CharField(u'难度', max_length=8)
    image= models.CharField(verbose_name=u'封面图片', blank=True,max_length=100)
    is_delete = models.BooleanField(u'是否删除',default=False)
    reserved1= models.CharField(u'备用1', max_length=100,blank=True)
    reserved2= models.CharField(u'备用2', max_length=100,blank=True)
    imagehost= models.CharField(u'宿主机IP', max_length=100,blank=True,null=True)
    repository= models.CharField(u'镜像名称', max_length=100,blank=True,null=True)
    index_port= models.CharField(u'起始端口', max_length=100,blank=True,null=True)

    class Meta:
        verbose_name = u'体系信息'
        verbose_name_plural = u"体系信息"
        permissions = (
            ("view_sysinfo",u"查看体系"),
            ("view_teach_manage",u"教学管理"),
        )


class Experinfo(models.Model):
    experid = models.AutoField(primary_key=True,verbose_name=u'实验id')
    name = models.CharField(u'体系名', max_length=20)
    introduction = models.CharField(u'体系描述', max_length=200,blank=True)
    duration= models.CharField(u'实验时长', max_length=100)
    createtime = models.DateTimeField(u'创建时间', auto_now_add = True)
    parent_id = models.IntegerField(u'父类id') 
    detail = models.TextField(u'实验详情',blank=True,default='')
    image= models.CharField(verbose_name=u'图片路径', blank=True,max_length=100,null=True)
    md_path= models.CharField(verbose_name=u'实验文档路径', blank=True,max_length=100,null=True)
    md_file= models.CharField(verbose_name=u'实验文件名', blank=True,max_length=100,null=True)
    creator= models.CharField(u'创建人', max_length=100,null=True)
    examine= models.BooleanField(u'是否考核',default=False)
    is_delete = models.BooleanField(u'是否删除',default=False)
    docker_info= models.CharField(u'docker备用', blank=True,max_length=100,null=True)
    container_info= models.CharField(u'容器备用', blank=True,max_length=100,null=True)
    reserved1= models.TextField(u'备用1', blank=True,default='')
    reserved2= models.CharField(u'备用2', max_length=100,blank=True,null=True)

    class Meta:
        verbose_name = u'实验信息'
        verbose_name_plural = u"实验信息"
        permissions = (
            ("view_experinfo",u"查看实验信息"),
            ("do_experiment",u"可做实验"),
        )            
