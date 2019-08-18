#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/11 15:50
# @Author  : luoxiaojian
# @Site    : 
# @File    : tags.py
# @Software: PyCharm
'''
增加前端显示的字符
'''
from django import template
register = template.Library()

@register.filter(name='group_str2')
def group_str2(group_list):
    '''
    功能：将角色列表转换为str
    :param group_list:
    :return:
    '''
    if len(group_list) < 3:
        return ' '.join([user.name for user in group_list])
    else:
        return '%s ... '% ' '.join([user.name for user in group_list[0:2]])

@register.filter(name='bool2str')
def bool2str(value):
    if value:
        return u'是'
    else:
        return u'否'

@register.filter(name='userlist_str2')
def userlist_str2(user_list):
    '''
    将用户列表转换为str
    :param user_list:
    :return:
    '''
    if len(user_list) < 3:
        return ' '.join([user.name_cn for user in user_list])
    else:
        return '%s ...' % ' '.join([user.name_cn for user in user_list[0:2]])

@register.filter(name='perm_str2')
def perm_str2(perm_list):
    """
    将用户或者租的权限列表转换为str
    """
    if len(perm_list) < 3:
        return ' '.join([perm.codename for perm in perm_list])
    else:
        return '%s ...' % ' '.join([perm.codename for perm in perm_list[0:2]])