from django.contrib import admin
from . import views
from django.urls import path,re_path
from users import user,group
app_name = 'users'
urlpatterns = [
    # path('users/list/',views.list,name='user_list'),
    #用户列表页
    path('users/list/',user.UserListView.as_view(),name='user_list'),
    # http://ip:8000/
    #首页
    path("", views.IndexView.as_view(), name='index'),
    #登录页面
    # http://ip:8000/login/
    path("login/", views.LoginView.as_view(), name='login'),
    #退出登录
    # http://ip:8000/logout/
    path("logout/", views.LogoutView.as_view(), name='logout'),
    #用户详情页
    re_path('userdetail/(?P<pk>[0-9]+)?/$',user.UserDetailView.as_view(),name='user_detail'),
    #修改用户密码
    path('modifypasswd/',user.ModifyPwdView.as_view(),name='modify_pwd'),
    #修改用户权限
    re_path('usergrouppower/(?P<pk>[0-9]+)?/$', user.UserGroupPowerView.as_view(), name='user_group_power'),
    ########组权限
    path("grouplist/", group.GroupListView.as_view(), name='role_list'),
    re_path("groupdetail/(?P<pk>[0-9]+)?/", group.GroupDetailView.as_view(), name='role_detail'),
    ######
]