#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/11 14:38
# @Author  : luoxiaojian
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
'''
将用户方面的View直接分离出来，新建文件夹，在文件夹的init里写相关的代码，需要注意的是要在url里需要注意相关的url
'''
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from pure_pagination.mixins import PaginationMixin

from users.forms import UserProfileForm
from users.models import UserProfile



class UserListView(LoginRequiredMixin,PaginationMixin,ListView):
    '''
    功能：用户管理形式
    '''
    login_url = '/login/'
    redirect_filed_name = 'redirect_to'

    model = UserProfile #相当于UserProfile.objects.all()
    template_name = 'users/user_list.html' #自定义模版文件
    context_object_name = 'users' #自定义传给前段模版渲染的变量，默认

    paginate_by = 3
    object = UserProfile

    '''
    功能：用户管理搜索功能
    '''
    def get_queryset(self):
        queryset = super(UserListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword','').strip()
        print(self.keyword)
        if self.keyword:
            queryset = queryset.filter(Q(name_cn__icontains=self.keyword)|Q(username__icontains=self.keyword))
        return queryset
    '''搜索框保留搜索字眼'''
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data()
        context['keyword'] = self.keyword
        return context
    
    def post(self,request):
        _userForm = UserProfileForm(request.POST)
        if _userForm.is_valid():
            try:
                _userForm.cleaned_data['password'] = make_password('123456')
                _userForm.cleaned_data['is_active'] = True
                data = _userForm.cleaned_data
                self.model.objects.create(**data)
                res = {'code':0,'result':'添加用户成功'}
            except:
                res = {'code': 1, 'result': '添加用户失败'}
        else:
            res = {'code': 1, 'result': _userForm.errors.as_json()}
        return JsonResponse(res,safe=True)

class UserDetailView(LoginRequiredMixin,DetailView):
    '''
    用户详情
    '''
    model = UserProfile
    template_name = 'users/user_edit.html'
    context_object_name = 'user'













