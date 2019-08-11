from django.contrib import admin
from . import views
from django.urls import path,re_path
from users import user
app_name = 'users'
urlpatterns = [
    # path('users/list/',views.list,name='user_list'),
    #用户列表页
    path('users/list/',user.UserListView.as_view(),name='user_list'),
    # http://ip:8000/
    path("", views.IndexView.as_view(), name='index'),
    # http://ip:8000/login/
    path("login/", views.LoginView.as_view(), name='login'),
    # http://ip:8000/logout/
    path("logout/", views.LogoutView.as_view(), name='logout'),
    #用户详情页
    re_path('userdetail/(?P<pk>[0-9]+)?/$',user.UserDetailView.as_view(),name='user_detail'),
    path('modifypasswd/',user.ModifyPwdView.as_view(),name='modify_pwd'),
    #角色管理
    re_path('usergrouppower/(?P<pk>[0-9]+)?/$', user.UserGroupPowerView.as_view(), name='user_group_power'),
]