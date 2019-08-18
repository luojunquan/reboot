from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, QueryDict
from django.urls import reverse
from django.views.generic import View, ListView, DetailView
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from pure_pagination.mixins import PaginationMixin


# 自定义模块导入
from .models import WorkOrder
from .forms import WorkOrderApplyForm, WorkOrderResultForm
from django.conf import settings

#工单申请列表
class WorkOrderApplyView(LoginRequiredMixin, View):
    def get(self, request):
        forms = WorkOrderApplyForm()
        return render(request, 'order/workorder_apply.html', {'forms': forms})

    def post(self, request):
        forms = WorkOrderApplyForm(request.POST or None, request.FILES or None)
        if forms.is_valid():
            try:
                print(forms.cleaned_data)
                title = forms.cleaned_data["title"]
                order_contents = forms.cleaned_data["order_contents"]
                assign = forms.cleaned_data["assign"]
                orderfiles = forms.cleaned_data["orderfiles"]

                work_order = WorkOrder()
                work_order.title = title
                work_order.order_contents = order_contents
                work_order.assign_id = assign
                work_order.orderfiles = orderfiles
                work_order.applicant = request.user
                work_order.status = 0
                work_order.save()
                return HttpResponseRedirect(reverse('workorder:list'))
            except:
                return render(request, 'order/workorder_apply.html', {'forms': forms, 'errmsg': '工单提交出错！'})
        else:
            return render(request, 'order/workorder_apply.html', {'forms': forms, 'errmsg': '工单填写格式出错！'})


class WorkOrderListView(LoginRequiredMixin, PaginationMixin, ListView):
    """
    待处理工单列表展示
    """
    model = WorkOrder
    template_name = 'order/workorder_list.html'
    context_object_name = "orderlist"
    paginate_by = 10
    keyword = ''

    def get_queryset(self):
        queryset = super(WorkOrderListView, self).get_queryset()
        # 只显示状态小于2，即申请和处理中的工单
        queryset = queryset.filter(status__lt=2)
        # 如果不是sa组的用户只显示自己申请的工单，别人看不到你申请的工单，管理员可以看到所有工单
        if 'OPS' not in [group.name for group in self.request.user.groups.all()]:
            queryset = queryset.filter(applicant=self.request.user)

        self.keyword = self.request.GET.get('keyword', '')
        if self.keyword:
            queryset = queryset.filter(Q(title__icontains = self.keyword)|
                                       Q(order_contents__icontains = self.keyword)|
                                       Q(result_desc__icontains=self.keyword))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(WorkOrderListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context


class WorkOrderDetailView(LoginRequiredMixin, DetailView):
    """
    工单详情页，包括处理结果表单的填写
    """
    model = WorkOrder
    template_name = "order/workorder_detail.html"
    context_object_name = "workorder"

    def post(self, request, **kwargs):
        pk = kwargs.get("pk")
        work_order = self.model.objects.get(pk=pk)

        if work_order.status == 0:
            work_order.status = 1
            work_order.handler = request.user
            work_order.save()
            return HttpResponseRedirect(reverse("workorder:list"))

        if work_order.status == 1:
            forms = WorkOrderResultForm(request.POST)
            if forms.is_valid():
                result_desc = request.POST.get('result_desc', '')
                work_order.result_desc = result_desc
                work_order.status = 2
                work_order.save()
                return HttpResponseRedirect(reverse('workorder:list'))
            else:
                return render(request, 'order/workorder_detail.html', {'work_order': work_order, 'errmsg': '必须填写处理结果！'})