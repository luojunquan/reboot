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