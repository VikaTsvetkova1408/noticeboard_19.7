from django.urls import path, include
from django.views.decorators.cache import cache_page
from . import views


app_name = 'core'

urlpatterns = [
    path('', views.CoreIndex.as_view(), name='notice_index'),
    path('add', views.NoticeAdd.as_view(), name='notice_add'),
    path('notice/<int:pk>', views.NoticeDetail.as_view(), name='notice_detail')
]
