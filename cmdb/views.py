import json
import time

import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, QueryDict, JsonResponse
from django.views import View
from django.views.generic import ListView

from cmdb.forms import CmdbsForm
from .models import Cmdbs
from pure_pagination.mixins import PaginationMixin

class CmdbListView(LoginRequiredMixin,PaginationMixin,ListView):
    model = Cmdbs
    template_name = 'cmdbs/host_list.html'  # 自定义模版文件
    context_object_name = 'objects'  # 自定义传给前段模版渲染的变量，默认
    paginate_by = 3

    '''功能：用户管理搜索功能'''
    def get_queryset(self):
        queryset = super(CmdbListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword','').strip()
        # print(self.keyword)
        if self.keyword:
            queryset = queryset.filter(Q(hostname__icontains=self.keyword)|Q(private_ip__icontains=self.keyword))
        return queryset

    '''搜索框保留搜索字眼'''
    def get_context_data(self, object_list=None, **kwargs):
        context = super(CmdbListView, self).get_context_data()
        context['keyword'] = self.keyword
        return context

    '''添加服务器信息'''
    def post(self,request):
        _cmdbForm = CmdbsForm(request.POST)
        if _cmdbForm.is_valid():
            try:
                # '''设置默认的CPU数和操作系统'''
                _cmdbForm.cleaned_data['vm_status'] = 1
                _cmdbForm.cleaned_data['manufacturers'] = 'innotek GmbH'
                _cmdbForm.cleaned_data['server_type'] = 'VirtualBox'
                _cmdbForm.cleaned_data['st'] = '0'
                _cmdbForm.cleaned_data['uuid'] = '27AAD645-1B17-49BD-A669-5309B69D8A69'
                _cmdbForm.cleaned_data['manufacture_date'] = '2006-01-12'
                '''
                # des: 最后输出type为  'datetime.datetime'
                str_time = '2019-04-04 08:00:00'
                result = datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S')
                '''
                createtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                #保存到数据库的时间类型为datetime，将str类型转换为datetime
                _cmdbForm.cleaned_data['create_time'] = datetime.datetime.strptime(createtime,'%Y-%m-%d %H:%M:%S.%f')
                _cmdbForm.cleaned_data['update_time'] = datetime.datetime.strptime(createtime,'%Y-%m-%d %H:%M:%S.%f')
                data = _cmdbForm.cleaned_data
                self.model.objects.create(**data)
                res = {'code':0,'result':'添加服务器信息成功'}
            except:
                print('==================')
                res = {'code': 1, 'result': '添加服务器信息失败'}
        else:
            res = {'code': 1, 'result': _cmdbForm.errors.as_json()}
            # print(res)
        return JsonResponse(res,safe=True)

    #删除服务器信息的逻辑，前端ajax处理
    def delete(self, request, **kwargs):
        cmdb_id = QueryDict(request.body).dict()
        try:
            Cmdbs.objects.filter(id=cmdb_id['id']).delete()
            ret = {'code': 0, 'result': '操作成功'}
        except BaseException:
            ret = {'code': 1, 'errmsg': '操作失败'}
        return JsonResponse(ret)

class CmdbDeleteView(View):
    '''
    功能：删除主机
    :param request:
    :param args:
    :param kwargs:
    :return:
    '''
    # Cmdbs.objects.get(id=kwargs['pk']).delete()
    # return redirect('cmdb:host_list')
    pass

class CmdbHostMapView(LoginRequiredMixin,ListView):

    model = Cmdbs
    template_name = 'cmdbs/hostmap.html'  # 自定义模版文件
    context_object_name = 'objects'  # 自定义传给前段模版渲染的变量，默认

def ticket_class_view_2(request):
    dataset = Cmdbs.objects \
        .values('ticket_class') \
        .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
                  not_survived_count=Count('ticket_class', filter=Q(survived=False))) \
        .order_by('ticket_class')

    categories = list()
    survived_series = list()
    not_survived_series = list()

    for entry in dataset:
        categories.append('%s Class' % entry['ticket_class'])
        survived_series.append(entry['survived_count'])
        not_survived_series.append(entry['not_survived_count'])

    return render(request, 'ticket_class_2.html', {
        'categories': json.dumps(categories),
        'survived_series': json.dumps(survived_series),
        'not_survived_series': json.dumps(not_survived_series)
    })

# class CollectHostInfo(View):
#
#     def get(self, request):
#         pass
#
#     def post(self, request):
#         import random
#         data = request.POST.dict()
#         data['hostname'] += str(random.randint(1, 100))
#         data['mac_address'] = "{} {}".format(str(random.randint(1, 100)), str(random.randint(1, 100)))
#         try:
#             Cmdbs.objects.create(**data)
#         except Exception as e:
#             print(e)
#         return HttpResponse("succ.")
