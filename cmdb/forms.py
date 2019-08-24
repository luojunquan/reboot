#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/11 16:46
# @Author  : luoxiaojian
# @Site    : 
# @File    : forms.py
# @Software: PyCharm
from django import forms
from django.contrib.auth.models import Group, Permission
from .models import Cmdbs
import re

# 添加用户表单验证
class CmdbsForm(forms.ModelForm):
    class Meta:
        model = Cmdbs
        # fields = "__all__"
        fields = ['hostname', 'private_ip', 'cpu','disk', 'mac_address','os']

    def clean_cpu(self):
        cpu = self.cleaned_data['cpu']
        return cpu

    def clean_os(self):
        os = self.cleaned_data['os']
        return os

    def clean_hostname(self):
        hostname = self.cleaned_data['hostname']
        return hostname

    def clean_disk(self):
        disk = self.cleaned_data['disk']
        return disk

    def clean_private_ip(self):
        '''
        正则匹配方法
        判断一个字符串是否是合法IP地址
        '''
        ip = self.cleaned_data['private_ip']
        compile_ip = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        p = re.compile(compile_ip)
        if p.match(ip):
            return ip
        else:
            raise forms.ValidationError('IP地址非法', code='invalid')

    def clean_mac_address(self):
        '''
        正则匹配方法
        判断一个字符串是否是合法MAC地址
        '''
        mac = self.cleaned_data['mac_address']
        compile_mac = re.compile(r'''
                          (^([0-9A-F]{1,2}[-]){5}([0-9A-F]{1,2})$
                          |^([0-9A-F]{1,2}[:]){5}([0-9A-F]{1,2})$
                          |^([0-9A-F]{1,2}[.]){5}([0-9A-F]{1,2})$)
                          ''',re.VERBOSE | re.IGNORECASE)
        p = re.compile(compile_mac)
        if p.match(mac):
            return mac
        else:
            raise forms.ValidationError('MAC地址非法', code='invalid')



# 更新用户表单验证
"""
UserProfileForm会联合model判断字段是否合法，同时也会检查数据库的唯一性索引，故而更新操作不能复用。
例如，更新一个 username=aa的用户，UserProfileForm先检查字段是否合法，然后检查数据库里有没有这个
用户。如果有则任务违反了唯一性索引，验证不通过。
"""


class UserUpdateForm(forms.Form):
    username = forms.CharField(required=True, max_length=10)
    name_cn = forms.CharField(required=True, max_length=30)
    phone = forms.CharField(required=True, max_length=11)

    def clean_phone(self):
        """
        通过正则表达式验证手机号码是否合法
        """
        phone = self.cleaned_data['phone']
        phone_regex = r'^1[34578][0-9]{9}$'
        p = re.compile(phone_regex)
        if p.match(phone):
            return phone
        else:
            # forms.ValidationError自定义表单错误
            raise forms.ValidationError('手机号码非法', code='invalid')