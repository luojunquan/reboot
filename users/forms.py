#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/11 16:46
# @Author  : luoxiaojian
# @Site    : 
# @File    : forms.py
# @Software: PyCharm
from django import forms
from django.contrib.auth.models import Group, Permission
from .models import UserProfile
import re

# 添加用户表单验证
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # fields = "__all__"
        fields = ['username', 'name_cn', 'phone']

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