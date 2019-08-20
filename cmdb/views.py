from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, QueryDict, JsonResponse
from django.views import View
from django.views.generic import ListView

from .models import Cmdbs
from pure_pagination.mixins import PaginationMixin

class CmdbListView(LoginRequiredMixin,PaginationMixin,ListView):
    model = Cmdbs
    template_name = 'cmdbs/host_list.html'  # 自定义模版文件
    context_object_name = 'objects'  # 自定义传给前段模版渲染的变量，默认
    paginate_by = 1

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

    #删除用户的逻辑，前端ajax处理
    def delete(self, request, **kwargs):
        cmdb_id = QueryDict(request.body).dict()
        print(cmdb_id)
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
