from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView
from pure_pagination import PaginationMixin

from users.models import UserProfile


class GroupListView(LoginRequiredMixin, PermissionRequiredMixin, PaginationMixin, ListView):
    '''
    查看组列表、添加组、删除组
    '''
    permission_required = ('users.admin',)
    model = Group
    template_name = 'users/group_list.html'
    context_object_name = 'grouplist'
    paginate_by = 2
    keyword = ''

    def get_queryset(self):
        queryset = super(GroupListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword','')
        if self.keyword:
            queryset = queryset.filter(name__icontains = self.keyword)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context


class GroupDetailView(LoginRequiredMixin, DetailView):
    """
    组详情
    """
    model = Group
    template_name = 'users/group_edit.html'
    context_object_name = "group"
    pk_url_kwarg = 'pk'

    # 返回所有权限，并将当前组所拥有的权限选中
    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        context['group_has_users'],context['group_has_permissions'] = self._get_group_permission()
        context['group_not_users'],context['group_not_permissions'] = self._get_group_not_permission()
        return context

    # 获取当前组所有权限，以列表形式返回
    def _get_group_permission(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        try:
            group = Group.objects.get(pk=pk)
            users = group.user_set.all()
            return users,group.permissions.all()
        except Group.DoesNotExist:
            raise Http404

    # 获取当前组没有的权限，以列表形式返回
    def _get_group_not_permission(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        try:
            group = self.model.objects.get(pk=pk)
            all_user = UserProfile.objects.all()
            users = [user for user in all_user if user not in group.user_set.all()]
            all_perms = Permission.objects.all()
            perms = [perm for perm in all_perms if perm not in group.permissions.all()]
            return users,perms
        except:
            return JsonResponse([], safe=False)

    #修改角色
    def post(self, request, **kwargs):
        #ops.user_set.set([2])
        print(request.POST)
        print(request.POST.getlist('users', []))
        user_id_list = request.POST.getlist('users_selected', [])
        permission_id_list = request.POST.getlist('perms_selected', [])
        pk = kwargs.get("pk")
        try:
            role = self.model.objects.get(pk=pk)
            # user.groups.set(group_id_list)
            print(user_id_list)
            role.user_set.set(user_id_list)
            role.permissions.set(permission_id_list)
            res = {'code': 0, 'next_url': reverse("users:role_list"), 'result': '角色权限更新成功'}
        except:
            res = {'code': 1, 'next_url': reverse("users:role_list"), 'errmsg': '角色权限更新失败'}
            #logger.error("edit  user group pwoer error: %s" % traceback.format_exc())
        return render(request, settings.JUMP_PAGE, res)