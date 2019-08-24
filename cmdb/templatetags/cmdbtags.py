#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/21 22:21
# @Author  : luoxiaojian
# @Site    : 
# @File    : tags.py
# @Software: PyCharm
from django import template
register = template.Library()

@register.filter(name='vmstatus')
def vmstatus(value):
    '''
    功能：转换服务器的状态
    :param value:
    :return:
    '''
    if value == 0:
        return u'在线线'
    elif value == 1:
        return u'下线'
    elif value == 2:
        return u'空闲中'