from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from users.models import UserProfile
from django.contrib.auth.hashers import make_password

# Create your views here.
'''
#将下面的代码替换成函数形式
def list(request,**kwargs):
    users = UserProfile.objects.all()
    return render(request, 'users/users_list.html', {'users':users})
'''

class LoginView(View):
    '''
    登录模块
    '''
    def get(self,request):
        return render(request, "login.html")

    def post(self,request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username,password=password)
        print(user)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('users:index'))
            else:
                return render(request, 'login.html', {'msg': "用户未激活"})
        return render(request, 'login.html', {'msg':"用户名或者密码错误"})

class IndexView(View):
    '''
    首页
    '''
    #2、第二种方法：login_required验证用户是否登陆
    '''
    # login_url 用户没有通过测试时跳转的地址，默认是 settings.LOGIN_URL
    @method_decorator(login_required(login_url='/login/'))
    '''
    # @method_decorator(login_required(login_url='/login/'))
    def get(self,request):
        '''
        #1、第一种方法：is_authenticated最原始的认证
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('users:login'))
        '''
        '''
        第三种方法：LoginRequiredMixin验证
        # 用户没有通过或者权限不够时跳转的地址，默认是 settings.LOGIN_URL.
        # 把没通过检查的用户重定向到没有 "next page" 的非登录页面时，把它设置为 None ，这样它会在 URL 中移除。
        redirect_field_name = 'redirect_to'   # http://123.56.73.115:8000/login/?redirect_to=/
        '''
        login_url = '/login/'
        redirect_field_name = 'redirect_to'  # http://123.56.73.115:8000/login/?redirect_to=/
        return render(request, 'index.html')

class LogoutView(View):
    '''
    登出功能
    '''
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse('users:login'))