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
from django.contrib.auth.models import Permission, Group
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect, QueryDict, Http404
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from pure_pagination.mixins import PaginationMixin

from reboot import settings
from users.forms import UserProfileForm, UserUpdateForm
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

    '''功能：用户管理搜索功能'''
    def get_queryset(self):
        queryset = super(UserListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword','').strip()
        # print(self.keyword)
        if self.keyword:
            queryset = queryset.filter(Q(name_cn__icontains=self.keyword)|Q(username__icontains=self.keyword))
        return queryset

    '''搜索框保留搜索字眼'''
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data()
        context['keyword'] = self.keyword
        return context

    '''添加用户'''
    def post(self,request):
        _userForm = UserProfileForm(request.POST)
        # data1 = QueryDict(request.body).dict()
        if _userForm.is_valid():
            try:
                '''设置默认的密码和默认激活'''
                _userForm.cleaned_data['password'] = make_password('123456')
                _userForm.cleaned_data['is_active'] = True
                data = _userForm.cleaned_data
                self.model.objects.create(**data)
                res = {'code':0,'result':'添加用户成功'}
            except:
                res = {'code': 1, 'result': '添加用户失败'}
        else:
            res = {'code': 1, 'result': _userForm.errors.as_json()}
            # print(res)
        return JsonResponse(res,safe=True)

    #删除用户的逻辑，前端ajax处理
    def delete(self, request, **kwargs):
        user_id = QueryDict(request.body).dict()
        try:
            UserProfile.objects.filter(pk=user_id['id']).delete()
            ret = {'code': 0, 'result': '操作成功'}
        except BaseException:
            ret = {'code': 1, 'errmsg': '操作失败'}
        return JsonResponse(ret)

#用户描述页，也可以修改用户信息
class UserDetailView(LoginRequiredMixin,DetailView):
    '''用户详情'''
    model = UserProfile
    template_name = 'users/user_edit.html'
    context_object_name = 'user'

    """更新用户信息"""
    def post(self, request, **kwargs):
        # print(request.POST)  # <QueryDict: {'id': ['7'], 'username': ['aa'], 'name_cn': ['bb'], 'phone': ['13305779168']}>
        # print(kwargs)  # {'pk': '7'}
        # print(request.body)  # b'id=7&username=aa&name_cn=bb&phone=13305779168'
        pk = kwargs.get("pk")
        data = QueryDict(request.body).dict()
        # print(data)  # {'id': '7', 'username': 'aa', 'name_cn': 'bb', 'phone': '13305779168'}
        _userForm = UserUpdateForm(request.POST)
        if _userForm.is_valid():
            try:
                self.model.objects.filter(pk=pk).update(**data)
                res = {'code': 0, "next_url": reverse("users:user_list"), 'result': '更新用户成功'}
            except:
                res = {'code': 1, "next_url": reverse("users:user_list"), 'errmsg': '更新用户失败'}

        else:
            # 获取所有的表单错误
            # print(_userForm.errors)
            res = {'code': 1, "next_url": reverse("users:user_list"), 'errmsg': _userForm.errors}
        return render(request, settings.JUMP_PAGE, res)

#修改密码页
class ModifyPwdView(LoginRequiredMixin,View):
    '''
    重置密码
    '''
    def get(self,request):
        uid = request.GET.get('uid',None)
        return render(request,'users/change_passwd.html',{'uid':uid})

    def post(self,request):
        uid = request.POST.get('uid',None)
        pwd1 = request.POST.get('password1',"")
        pwd2 = request.POST.get('password2', "")
        if pwd1 != pwd2:
            return render(request,'users/change_passwd.html',{'msg':'两次密码不一致'})
        try:
            user = UserProfile.objects.get(pk=uid)
            user.password = make_password(pwd1)
            user.save()
            return HttpResponseRedirect(reverse('users:index'))
        except:
            return render(request,"users/change_passwd.html",{'msg':'密码修改失败'})

#用户权限页
class UserGroupPowerView(LoginRequiredMixin, DetailView):
    '''
    更新用户角色及权限
    '''
    template_name = 'users/user_group_power.html'
    model = UserProfile
    context_object_name = 'user'

    # 返回所有组、权限，并将当前用户所拥有的组、权限显示
    def get_context_data(self, **kwargs):
        context = super(UserGroupPowerView, self).get_context_data(**kwargs)
        context['user_has_groups'], context['user_has_permissions'] = self._get_user_group_power()
        context['user_not_groups'], context['user_not_permissions'] = self._get_user_not_group_power()
        return context

    # 获取当前用户所有组、权限以列表形式返回
    def _get_user_group_power(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        try:
            user = self.model.objects.get(pk=pk)
            return user.groups.all(), user.user_permissions.all()
        except self.model.DoesNotExist:
            raise Http404

    # 获取当前用户没有的组、权限，以列表形式返回
    def _get_user_not_group_power(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        try:
            user = self.model.objects.get(pk=pk)
            all_group = Group.objects.all()
            groups = [group for group in all_group if group not in user.groups.all()]
            all_perms = Permission.objects.all()
            perms = [perm for perm in all_perms if perm not in user.user_permissions.all()]
            return groups, perms
        except:
            return JsonResponse([], safe=False)

    def post(self, request, **kwargs):
        group_id_list = request.POST.getlist('groups_selected', [])
        permission_id_list = request.POST.getlist('perms_selected', [])
        pk = kwargs.get("pk")
        try:
            user = self.model.objects.get(pk=pk)
            user.groups.set(group_id_list)
            user.user_permissions.set(permission_id_list)
            res = {'code': 0, 'next_url': reverse("users:user_list"), 'result': '用户角色权限更新成功'}
        except:
            res = {'code': 1, 'next_url': reverse("users:user_list"), 'errmsg': '用户角色权限更新失败'}
        return render(request, settings.JUMP_PAGE, res)










