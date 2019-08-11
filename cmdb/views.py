from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.views import View
from .models import Cmdbs

import logging
logger = logging.getLogger("collect")

class CmdbView(View):
    def get(self,request,*args,**kwargs):
        objs = Cmdbs.objects.all()
        print(objs)
        return render(request, 'cmdbs/host_list.html', context={'objects' : objs})

def CmdbDeleteView(request,*args,**kwargs):
    '''
    功能：删除主机
    :param request:
    :param args:
    :param kwargs:
    :return:
    '''
    Cmdbs.objects.get(id=kwargs['pk']).delete()
    return redirect('cmdb:host_list')

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
