from .views import *
from django.urls import path,re_path
app_name = 'workorder'
urlpatterns = [
    path("apply/",WorkOrderApplyView.as_view(),name='apply'),
    path("list/",WorkOrderListView.as_view(),name='list'),
    re_path('detail/(?P<pk>[0-9]+)?/',WorkOrderDetailView.as_view(),name='detail'),
]