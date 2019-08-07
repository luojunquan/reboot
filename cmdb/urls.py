from django.contrib import admin
from . import views
from django.urls import path,re_path
from django.conf.urls import url

app_name = 'cmdb'
urlpatterns = [
    # http://ip:8000/
    # path("", views.IndexView.as_view(), name='index'),
    #http://127.0.0.1:8000/host_list/
    path("host_list/", views.CmdbView.as_view(), name='host_list'),
    #正则表达式匹配
    re_path('host_delete/(?P<pk>[0-9]+)/$', views.CmdbDeleteView),
]