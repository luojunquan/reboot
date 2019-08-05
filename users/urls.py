from django.contrib import admin
from . import views
from django.urls import path,re_path

app_name = 'users'
urlpatterns = [
    path('users/list/',views.list,name='user_list'),
    # http://ip:8000/
    path("", views.IndexView.as_view(), name='index'),
    # http://ip:8000/login/
    path("login/", views.LoginView.as_view(), name='login'),
    # http://ip:8000/logout/
    path("logout/", views.LogoutView.as_view(), name='logout'),
]